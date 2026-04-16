"""Example Flower server wiring with a small HUD state API.

Run with `--serve` to expose a static file server plus `/api/v1/hud/state`.
"""

from __future__ import annotations

import argparse
import json
import os
from datetime import datetime, timezone
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

from security_wrapper import build_secure_fedavg, load_policy
from security_wrapper.policy import resolve_policy_path


REPO_ROOT = Path(__file__).resolve().parents[1]


def build_secure_strategy(policy_path: str | None = None):
    selected_policy = policy_path or resolve_policy_path("policy.rare_disease.json")
    return build_secure_fedavg(
        policy_path=selected_policy,
        fraction_fit=1.0,
        fraction_evaluate=0.0,
        min_fit_clients=2,
        min_available_clients=2,
    )


def _policy_profile(policy_path: str) -> str:
    stem = Path(policy_path).stem.lower()
    if "rare_disease" in stem:
        return "RARE-DISEASE"
    if "example" in stem:
        return "EXAMPLE"
    return stem.replace("_", "-").upper()


def build_hud_state(policy_path: str | None = None) -> dict[str, object]:
    selected_policy = resolve_policy_path(policy_path or "policy.rare_disease.json")
    policy = load_policy(selected_policy)
    alert_source = policy.siem_webhook_url or policy.siem_webhook_url_env or "governance-contract"
    node_count = 47
    healthy_nodes = 31

    return {
        "policy_profile": _policy_profile(selected_policy),
        "policy_file": selected_policy,
        "attestation_mode": str(policy.attestation_mode or "metric_flag"),
        "nonce_store_mode": str(policy.nonce_store_mode or "memory"),
        "alert_source": str(alert_source),
        "node_coverage": {
            "total_nodes": node_count,
            "healthy_nodes": healthy_nodes,
            "region_count": 7,
            "coverage_label": "Coverage: 47 simulated nodes across 7 regions",
        },
        "source": "flower_security_wrapper/example_server.py",
        "updated_at": datetime.now(timezone.utc).isoformat(),
    }


class DemoRequestHandler(SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=str(REPO_ROOT), **kwargs)

    def do_GET(self):
        if self.path.split("?", 1)[0] == "/api/v1/hud/state":
            payload = build_hud_state(os.getenv("FLWR_POLICY_FILE"))
            body = json.dumps(payload, indent=2).encode("utf-8")
            self.send_response(200)
            self.send_header("Content-Type", "application/json; charset=utf-8")
            self.send_header("Content-Length", str(len(body)))
            self.send_header("Cache-Control", "no-store")
            self.end_headers()
            self.wfile.write(body)
            return

        super().do_GET()

    def log_message(self, format, *args):
        return


def serve(host: str = "127.0.0.1", port: int = 8080) -> None:
    server = ThreadingHTTPServer((host, port), DemoRequestHandler)
    print(f"Serving demo assets and HUD state on http://{host}:{port}")
    print(f"HUD state endpoint: http://{host}:{port}/api/v1/hud/state")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("Shutting down demo server...")
    finally:
        server.server_close()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Sovereign MOHAWK example server")
    parser.add_argument("--serve", action="store_true", help="serve static demo assets and HUD state")
    parser.add_argument("--host", default="127.0.0.1", help="host to bind when serving")
    parser.add_argument("--port", default=8080, type=int, help="port to bind when serving")
    parser.add_argument("--print-strategy", action="store_true", help="print the wrapped Flower strategy instead of serving")
    args = parser.parse_args()

    if args.serve or not args.print_strategy:
        serve(args.host, args.port)
    else:
        strategy = build_secure_strategy(os.getenv("FLWR_POLICY_FILE"))
        print("Secure strategy wrapper ready:", strategy)
