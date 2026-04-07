# Flower Security Wrapper

This package adds a policy enforcement layer around a Flower-like strategy.
It is the backend security and governance component of the full-stack Sovereign MOHAWK platform.

Related full-stack surfaces:

- Dashboard application: `../index.html`
- Frontend orchestration and WAL controls: `../app.js`
- Compliance and beta evidence docs: `../docs/beta/COMPLIANCE_EVIDENCE.md`

## What it enforces

- Client allowlist checks
- Ed25519 signature verification (or metric flag fallback)
- Attestation checks (`metric_flag` or signed quote verification)
- Round-bound nonce replay protection with durable stores (`sqlite`, `redis`, `postgres`)
- Differential privacy budget threshold checks
- Payload size limits
- Gradient poisoning detection using z-score and consensus checks (cosine + Krum-style)
- Structured audit logging for accepted/rejected updates
- Hash-chained WAL ledger with CRC integrity checks and replay support
- Smart-contract-style governance gate evaluation (automated, no synchronous reviewer bottleneck)
- Automatic slashing and quarantine for malicious or policy-violating clients
- Optional SIEM webhook forwarding and repeated-strike alert events

## Files

- `security_wrapper/wrapper.py`: Strategy wrapper
- `security_wrapper/checks.py`: Policy checks
- `security_wrapper/crypto.py`: Ed25519 verifier and canonical message builder
- `security_wrapper/attestation.py`: Attestation verifier (metric flag or signed quote)
- `security_wrapper/nonce_store.py`: In-memory, SQLite, Redis, and Postgres nonce stores
- `security_wrapper/poisoning.py`: Cosine and Krum-style poisoning detectors
- `security_wrapper/siem.py`: SIEM webhook forwarder and strike-pattern alerter
- `security_wrapper/flwr_integration.py`: Concrete `FedAvg` secure integration
- `security_wrapper/policy.py`: Policy model and loader
- `security_wrapper/governance_contract.py`: Governance gate contract + slashing ledger
- `security_wrapper/audit.py`: JSONL audit logger
- `security_wrapper/wal_ledger.py`: Append-only write-ahead ledger with tamper checks
- `security_wrapper/rejection_codes.py`: Rejection taxonomy
- `policy.example.json`: Example policy
- `policy.rare_disease.json`: Rare-disease-first profile (stricter DP + faster quarantine)
- `example_server.py`: Integration skeleton
- `adversarial_exercise.py`: 1 benign + 2 malicious staging simulation

## Quick start

1. Copy and customize `policy.example.json`.
2. Wrap your Flower strategy:

```python
from security_wrapper import build_secure_fedavg

secure_strategy = build_secure_fedavg(
  policy_path="policy.example.json",
  min_fit_clients=2,
  min_available_clients=2,
)
```

1. Use `secure_strategy` in your Flower server startup.

## Beta Packaging and CI

Package metadata is defined in [pyproject.toml](pyproject.toml).

CI and release automation lives at repository root:

- [.github/workflows/ci.yml](../.github/workflows/ci.yml)
- [.github/workflows/beta-artifacts.yml](../.github/workflows/beta-artifacts.yml)

These workflows produce beta artifacts including:

- `junit.xml`
- `coverage.xml`
- `dist/*.whl` and `dist/*.tar.gz`
- policy snapshots and git evidence files

## Environment-based secret loading

To avoid storing public key registries and SIEM endpoints directly in policy files,
the loader supports env-based injection.

Example environment variables:

```bash
export FLWR_CLIENT_PUBLIC_KEYS_JSON='{"hospital-eu-01":"<hex>","hospital-us-02":"<hex>"}'
export FLWR_ATTESTATION_PUBLIC_KEYS_JSON='{"hospital-eu-01":"<hex>","hospital-us-02":"<hex>"}'
export FLWR_SIEM_WEBHOOK_URL='https://siem.example.org/events'
```

Rare disease profile equivalents:

```bash
export FLWR_RD_CLIENT_PUBLIC_KEYS_JSON='{"hospital-rd-01":"<hex>","hospital-rd-02":"<hex>"}'
export FLWR_RD_ATTESTATION_PUBLIC_KEYS_JSON='{"hospital-rd-01":"<hex>","hospital-rd-02":"<hex>"}'
export FLWR_RD_SIEM_WEBHOOK_URL='https://siem.example.org/rare-disease/events'
```

## Required client metrics

Each client update should provide these metrics:

- `client_id`
- `signature_verified` (bool)
- `attestation_ok` (bool)
- `epsilon_spent` (float)
- `payload_size_bytes` (int)
- `nonce` (unique per update)
- `payload_hash` (hash of model update payload)
- `signature_hex` (hex Ed25519 signature over canonical message)

If any check fails, the update is rejected and logged with a rejection reason.

When governance contract mode is enabled, gate failures are also recorded with
deterministic reason strings and the client is automatically slashed according to
policy.

Canonical signed message format:

`client_id|server_round|nonce|payload_hash`

## Pentest simulation tests

Run pentest-style validation from this package root:

```bash
python -m unittest discover -s tests -p "test_*.py" -v
```

Included attack simulations cover:

- Replay nonce attacks
- Forged signature attempts
- Differential privacy budget abuse
- Oversized payload injection
- Gradient anomaly poisoning attempts
- Contract slashing and quarantine thresholds

SIEM webhook ingestion is validated by test coverage in `tests/test_siem.py`.
TPM quote parsing/freshness/PCR checks are covered in `tests/test_attestation.py`.

To run a live adversarial staging simulation:

```bash
python adversarial_exercise.py
```

## Compliance Mapping Reference

See beta compliance evidence docs at:

- [../docs/beta/COMPLIANCE_EVIDENCE.md](../docs/beta/COMPLIANCE_EVIDENCE.md)

This wrapper's controls support HIPAA/GDPR-aligned beta enforcement and auditability.
