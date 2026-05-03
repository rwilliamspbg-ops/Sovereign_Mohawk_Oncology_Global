import time
from typing import Any, Callable, Dict, List, Optional, Set, Tuple, cast

from .audit import AuditLogger
from .attestation import AttestationVerifier
from .checks import evaluate_update
from .crypto import Ed25519Verifier
from .governance_contract import GovernanceGateContract
from .nonce_store import (
    InMemoryNonceStore,
    NonceStore,
    PostgresNonceStore,
    RedisNonceStore,
    SqliteNonceStore,
)
from .policy import SecurityPolicy
from .poisoning import detect_poisoned_clients
from .rejection_codes import RejectionCode
from .siem import StrikePatternAlerter, WebhookSiemForwarder


def _percentile(values: List[float], q: float) -> float:
    if not values:
        return 0.0
    if len(values) == 1:
        return values[0]
    sorted_vals = sorted(values)
    pos = max(0.0, min(1.0, q)) * (len(sorted_vals) - 1)
    lower = int(pos)
    upper = min(lower + 1, len(sorted_vals) - 1)
    weight = pos - lower
    return sorted_vals[lower] * (1.0 - weight) + sorted_vals[upper] * weight


class SecurityWrapperStrategy:
    """
    Wrap a Flower-like strategy and enforce policy checks in aggregate_fit.

    Expected behavior:
    - inner_strategy has an aggregate_fit(server_round, results, failures) method
    - each fit result has a metrics dictionary
    """

    def __init__(
        self,
        inner_strategy: Any,
        policy: SecurityPolicy,
        audit_logger: Optional[AuditLogger] = None,
        signature_verifier: Optional[Ed25519Verifier] = None,
        attestation_verifier: Optional[AttestationVerifier] = None,
        nonce_store: Optional[NonceStore] = None,
        benchmark_hook: Optional[Callable[[Dict[str, object]], None]] = None,
    ) -> None:
        self.inner_strategy = inner_strategy
        self.policy = policy
        self.siem_forwarder = WebhookSiemForwarder(
            endpoint=self.policy.siem_webhook_url or None,
            timeout_seconds=self.policy.siem_timeout_seconds,
        )
        self.audit = audit_logger or AuditLogger(
            "security_audit.jsonl", forwarder=self.siem_forwarder
        )
        self.seen_round_nonces: Set[Tuple[int, str]] = set()
        if nonce_store is not None:
            self.nonce_store = nonce_store
        elif self.policy.nonce_store_mode == "sqlite":
            self.nonce_store = SqliteNonceStore(self.policy.nonce_sqlite_path)
        elif self.policy.nonce_store_mode == "redis":
            self.nonce_store = RedisNonceStore(self.policy.nonce_redis_url)
        elif self.policy.nonce_store_mode == "postgres":
            self.nonce_store = PostgresNonceStore(
                dsn=self.policy.nonce_postgres_dsn,
                table_name=self.policy.nonce_postgres_table,
            )
        else:
            self.nonce_store = InMemoryNonceStore()
        self.signature_verifier = signature_verifier or Ed25519Verifier()
        self.attestation_verifier = attestation_verifier or AttestationVerifier(
            mode=self.policy.attestation_mode,
            max_age_seconds=self.policy.attestation_max_age_seconds,
            expected_pcrs=self.policy.attestation_expected_pcrs,
            require_nonce_binding=self.policy.attestation_require_nonce_binding,
            signature_mode=self.policy.attestation_signature_mode,
            allow_metric_fallback=self.policy.allow_attestation_metric_fallback,
        )
        self.strike_alerter = StrikePatternAlerter(
            threshold=self.policy.siem_strike_alert_threshold,
            window_minutes=15,
        )
        self.governance_contract = GovernanceGateContract(
            required_gates=self.policy.governance_required_gates,
            readiness_required_signals=self.policy.governance_readiness_signals,
            initial_stake=self.policy.initial_stake,
            slash_amounts=self.policy.slash_amounts or None,
            strike_quarantine_threshold=self.policy.strike_quarantine_threshold,
        )
        self.benchmark_hook = benchmark_hook

    def __getattr__(self, name: str) -> Any:
        # Forward unsupported methods/attributes to the wrapped strategy.
        return getattr(self.inner_strategy, name)

    def aggregate_fit(
        self,
        server_round: int,
        results: List[Tuple[Any, Any]],
        failures: List[Any],
    ) -> Any:
        round_start = time.perf_counter()
        accepted: List[Tuple[Any, Any]] = []
        poisoned_clients: Set[str] = set()
        governance_rejections = 0
        poisoning_rejections = 0
        validation_rejections = 0
        client_eval_elapsed_ms: List[float] = []

        if self.policy.require_vector_consensus_checks:
            vectors: Dict[str, List[float]] = {}
            for _, fit_res in results:
                metrics = dict(getattr(fit_res, "metrics", {}) or {})
                client_id = str(metrics.get("client_id", "unknown"))
                vec = metrics.get("gradient_vector")
                if isinstance(vec, list) and vec:
                    numeric_vec: List[float] = []
                    valid_vec = True
                    vec_list = cast(List[Any], vec)
                    for entry in vec_list:
                        if isinstance(entry, (int, float)):
                            numeric_vec.append(float(entry))
                        else:
                            valid_vec = False
                            break
                    if valid_vec and numeric_vec:
                        vectors[client_id] = numeric_vec

            poisoned_clients = detect_poisoned_clients(
                vectors,
                min_cosine_similarity=self.policy.min_gradient_cosine_similarity,
                max_krum_score=self.policy.max_krum_score,
            )

        for client_proxy, fit_res in results:
            client_eval_start = time.perf_counter()
            metrics = dict(getattr(fit_res, "metrics", {}) or {})
            client_id = str(metrics.get("client_id", "unknown"))

            if client_id in poisoned_clients:
                poisoning_rejections += 1
                slash_state = self.governance_contract.slash(
                    client_id, RejectionCode.POISONING_ANOMALY
                )
                self.audit.log(
                    "update_rejected_poisoning",
                    {
                        "round": server_round,
                        "client_id": client_id,
                        "reason": RejectionCode.POISONING_ANOMALY.value,
                        "stake": slash_state["stake"],
                        "strikes": slash_state["strikes"],
                        "quarantined": slash_state["quarantined"],
                    },
                )
                client_eval_elapsed_ms.append(
                    (time.perf_counter() - client_eval_start) * 1000.0
                )
                continue

            if self.policy.enable_governance_contract:
                governance_decision = self.governance_contract.evaluate(
                    client_id=client_id,
                    metrics=metrics,
                    dp_limit=self.policy.max_epsilon_spent_per_round,
                )
                if not governance_decision.accepted:
                    governance_rejections += 1
                    slash_state = self.governance_contract.slash(
                        client_id, RejectionCode.POLICY_ERROR
                    )
                    self.audit.log(
                        "update_rejected_governance",
                        {
                            "round": server_round,
                            "client_id": client_id,
                            "reason": governance_decision.reason,
                            "gates": governance_decision.gates,
                            "stake": slash_state["stake"],
                            "strikes": slash_state["strikes"],
                            "quarantined": slash_state["quarantined"],
                        },
                    )
                    client_eval_elapsed_ms.append(
                        (time.perf_counter() - client_eval_start) * 1000.0
                    )
                    continue

            ok, rejection = evaluate_update(
                metrics,
                self.policy,
                self.seen_round_nonces,
                server_round=server_round,
                verifier=self.signature_verifier,
                attestation_verifier=self.attestation_verifier,
                nonce_store=self.nonce_store,
            )
            if ok:
                accepted.append((client_proxy, fit_res))
                stake_state = self.governance_contract.reward(client_id)
                self.audit.log(
                    "update_accepted",
                    {
                        "round": server_round,
                        "client_id": client_id,
                        "nonce": metrics.get("nonce"),
                        "epsilon_spent": metrics.get("epsilon_spent"),
                        "payload_size_bytes": metrics.get("payload_size_bytes"),
                        "stake": stake_state["stake"],
                    },
                )
            else:
                validation_rejections += 1
                slash_state = {
                    "stake": None,
                    "strikes": None,
                    "quarantined": None,
                }
                if self.policy.slashing_enabled and rejection is not None:
                    slash_state = self.governance_contract.slash(client_id, rejection)
                    if self.strike_alerter.record(client_id):
                        self.audit.log(
                            "siem_alert",
                            {
                                "round": server_round,
                                "client_id": client_id,
                                "alert": "repeated_strike_pattern",
                                "strikes": slash_state["strikes"],
                            },
                        )

                self.audit.log(
                    "update_rejected",
                    {
                        "round": server_round,
                        "client_id": client_id,
                        "reason": str(rejection or RejectionCode.POLICY_ERROR),
                        "nonce": metrics.get("nonce"),
                        "stake": slash_state["stake"],
                        "strikes": slash_state["strikes"],
                        "quarantined": slash_state["quarantined"],
                    },
                )

            client_eval_elapsed_ms.append(
                (time.perf_counter() - client_eval_start) * 1000.0
            )

        if not accepted:
            self.audit.log(
                "round_rejected",
                {
                    "round": server_round,
                    "reason": "no_updates_passed_security_policy",
                },
            )

        if self.policy.emit_round_benchmarks:
            client_eval_p95_ms = round(_percentile(client_eval_elapsed_ms, 0.95), 3)
            p95_budget = float(self.policy.benchmark_client_eval_p95_budget_ms)
            p95_within_budget = True
            if p95_budget > 0.0:
                p95_within_budget = client_eval_p95_ms <= p95_budget

            benchmark_payload: Dict[str, object] = {
                "round": server_round,
                "total_results": len(results),
                "accepted": len(accepted),
                "rejected": len(results) - len(accepted),
                "rejected_poisoning": poisoning_rejections,
                "rejected_governance": governance_rejections,
                "rejected_validation": validation_rejections,
                "elapsed_ms": round((time.perf_counter() - round_start) * 1000.0, 3),
                "avg_client_eval_ms": round(
                    sum(client_eval_elapsed_ms) / len(client_eval_elapsed_ms), 3
                )
                if client_eval_elapsed_ms
                else 0.0,
                "p95_client_eval_ms": client_eval_p95_ms,
                "p95_budget_ms": p95_budget,
                "p95_within_budget": p95_within_budget,
            }
            self.audit.log("round_benchmark", benchmark_payload)

            if p95_budget > 0.0 and not p95_within_budget:
                self.audit.log(
                    "round_benchmark_slo_violation",
                    {
                        "round": server_round,
                        "metric": "p95_client_eval_ms",
                        "value": client_eval_p95_ms,
                        "budget_ms": p95_budget,
                    },
                )

            if self.benchmark_hook is not None:
                try:
                    self.benchmark_hook(benchmark_payload)
                except Exception:
                    # Observability hooks must not block training rounds.
                    pass

        return self.inner_strategy.aggregate_fit(server_round, accepted, failures)
