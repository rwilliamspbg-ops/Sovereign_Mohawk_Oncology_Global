# Sovereign_Mohawk_Oncology_Global

a comprehensive healthcare app for cancer and disease research with full HIPAA/GDPR compliance mapping

## Local Run

This repository now includes a standalone interactive dashboard:

- `index.html`
- `styles.css`
- `app.js`

Run it locally with any static file server:

```bash
cd /workspaces/Sovereign_Mohawk_Oncology_Global
python3 -m http.server 8080
```

Then open `http://localhost:8080` in your browser.

## Included Modules

- Dashboard with 47-node global map simulation and FL stage interaction
- Research Trials view with drill-down rows and disease filtering
- FL Pipeline with live MOHAWK runtime-style log stream and capability allow/block lists
- HIPAA/GDPR control mapping table (10 controls)
- Security architecture cards (Wasmtime, TPM, Ed25519, DP, SecAgg, zero-trust)
- Consent management toggles
- Prometheus metrics simulator:
  - Feed switcher: FL Throughput, Epsilon Consumption, Round Latency P95, Node Health
  - Time window switcher: 30s / 1m / 5m
  - Dynamic alarm state: normal/warn/critical
  - Regional availability and sandbox violation indicators
- GDPR DPIA Generator (5 steps):
  - Processing description
  - Necessity and proportionality checks
  - Risk assessment
  - Data subject rights
  - Supervisory authority consultation trigger
  - Validation and report generation
- LLM Input Workflow:
  - Model registry form with provider/task/risk profile capture
  - Prompt-template validator with placeholder and identifier checks
  - Governance gate checklist with readiness evaluation
  - Execution audit viewer with simulated trace events
  - Helper buttons and auto-tuners for safer defaults and control tuning
- Assistance Agent + Threat Analysis:
  - Assistance agent mode switcher for research planning, protocol review, and compliance review
  - Smart helper prompt loader and automated review packet generator
  - Confidence-scored assistance output tied to platform status indicators
  - STRIDE-style overall threat analysis table with dynamic scoring
  - Mitigation auto-tuner that adjusts threat posture based on governance and PHI controls
- Professor Plan:
  - 90-day roadmap controller (Weeks 0-2, 3-6, 7-12) with translational milestones
  - Plug-and-play equipment matrix for lean, mid-scale, and comprehensive centers
  - Standards/governance completion checklist with required-coverage scoring
  - Procurement and pilot auto-builder with CAPEX estimates and PI executive brief generation
- Security Gold Standard Operations:
  - Today Action Sprint checklist with auto-apply for feasible immediate controls
  - Control scorecard across zero trust, attestation, key management, supply chain, runtime, SOC, and LLM safety
  - 30/60/90 security roadmap views with phase-specific priorities
  - Security SLO tracker and escalation pack generator for critical metric gaps

## Notes

- Runtime and metrics are simulated in-browser for demo/testing.
- No PHI or external APIs are used in this prototype.

## Flower Security Wrapper

A concrete Flower security wrapper skeleton is included in [flower_security_wrapper/README.md](flower_security_wrapper/README.md).

This wrapper adds policy-gated update admission, rejection taxonomy, and immutable JSONL audit events for federated training rounds.

## Beta Build and Release

This repository now includes Beta release automation for CI, package builds, Pages demo deployment, and evidence artifacts.

### GitHub Workflows

- [CI](.github/workflows/ci.yml): lint, tests, pentest simulations, coverage, package build, artifact upload
- [Deploy Demo to GitHub Pages](.github/workflows/pages.yml): deploys `index.html`, `styles.css`, and `app.js`
- [Beta Artifact Capture](.github/workflows/beta-artifacts.yml): captures release evidence bundles on `beta-*` tags or manual dispatch

### Package Build

Python package metadata for the Flower wrapper is in [flower_security_wrapper/pyproject.toml](flower_security_wrapper/pyproject.toml).

Local build:

```bash
cd flower_security_wrapper
python -m pip install --upgrade pip
pip install -r requirements-dev.txt
python -m build
```

### GitHub Pages Demo

After `main` workflow deployment, the dashboard is available on GitHub Pages at:

`https://<owner>.github.io/Sovereign_Mohawk_Oncology_Global/`

### Beta Compliance Evidence

Compliance and control-evidence docs:

- [Beta Release Plan](docs/beta/BETA_RELEASE.md)
- [Compliance Evidence](docs/beta/COMPLIANCE_EVIDENCE.md)

These capture how Beta controls map to:

- HIPAA 164.502 / 164.514 / 164.312 / 164.312(b)
- GDPR Art.5 / 25 / 30 / 32 / 89

### Artifact Capture

Artifact capture helper:

- [scripts/capture_beta_artifacts.sh](scripts/capture_beta_artifacts.sh)

Generated artifacts include:

- policy snapshots
- git commit/status evidence
- test/build outputs from workflows (`junit.xml`, `coverage.xml`, `dist/*`)
