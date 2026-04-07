# Sovereign_Mohawk_Oncology_Global

[![CI](https://github.com/rwilliamspbg-ops/Sovereign_Mohawk_Oncology_Global/actions/workflows/ci.yml/badge.svg)](https://github.com/rwilliamspbg-ops/Sovereign_Mohawk_Oncology_Global/actions/workflows/ci.yml)
[![Pages](https://github.com/rwilliamspbg-ops/Sovereign_Mohawk_Oncology_Global/actions/workflows/pages.yml/badge.svg)](https://github.com/rwilliamspbg-ops/Sovereign_Mohawk_Oncology_Global/actions/workflows/pages.yml)
[![Beta Artifacts](https://github.com/rwilliamspbg-ops/Sovereign_Mohawk_Oncology_Global/actions/workflows/beta-artifacts.yml/badge.svg)](https://github.com/rwilliamspbg-ops/Sovereign_Mohawk_Oncology_Global/actions/workflows/beta-artifacts.yml)
[![Release Drafter](https://github.com/rwilliamspbg-ops/Sovereign_Mohawk_Oncology_Global/actions/workflows/release-drafter.yml/badge.svg)](https://github.com/rwilliamspbg-ops/Sovereign_Mohawk_Oncology_Global/actions/workflows/release-drafter.yml)
[![Python 3.12](https://img.shields.io/badge/python-3.12-3776AB?logo=python&logoColor=white)](flower_security_wrapper/pyproject.toml)
[![Stack: Full](https://img.shields.io/badge/stack-HTML%2FCSS%2FJS%20%2B%20Python%203.12-1f6feb)](README.md)
[![Protocol: Flower FL](https://img.shields.io/badge/protocol-Flower%20FL-1f6feb)](flower_security_wrapper/README.md)
[![Package: beta](https://img.shields.io/badge/package-0.1.0b1-orange)](flower_security_wrapper/pyproject.toml)
[![Security Profile: HIPAA-GDPR](https://img.shields.io/badge/security-HIPAA%20%7C%20GDPR-0a7b83)](docs/beta/COMPLIANCE_EVIDENCE.md)
[![Ledger: WAL](https://img.shields.io/badge/ledger-hash--chained%20WAL-0a7b83)](flower_security_wrapper/security_wrapper/wal_ledger.py)
[![License: MIT](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![Manifesto](https://img.shields.io/badge/Manifesto-Genesis%20v1.0-black)](manifesto.html)

a comprehensive healthcare app for cancer and disease research with full HIPAA/GDPR compliance mapping

## Full-Stack Scope

This repository is a full-stack platform spanning frontend operations UX and backend federated security enforcement:

- Frontend layer: interactive browser dashboard in `index.html`, `styles.css`, and `app.js` with workflow modules for trials, compliance, metrics, governance, and WAL simulation.
- Backend security layer: Python Flower security wrapper in `flower_security_wrapper/security_wrapper` covering policy checks, attestation, signature controls, slashing logic, SIEM forwarding, and WAL persistence.
- Verification layer: CI/workflow-driven lint, tests, artifact capture, and beta compliance evidence under `docs/beta`.

## Pinned: Genesis Manifesto

Read the formal onboarding document: [The Genesis Manifesto: Sovereign Mohawk Ecosystem](manifesto.html)

Source markdown: [docs/GENESIS_MANIFESTO.md](docs/GENESIS_MANIFESTO.md)

Key references:

- Protocol implementation: [flower_security_wrapper/README.md](flower_security_wrapper/README.md)
- Compliance evidence: [docs/beta/COMPLIANCE_EVIDENCE.md](docs/beta/COMPLIANCE_EVIDENCE.md)
- Global map dashboard: [index.html](index.html)

## Standout Capabilities

- Flower Security Wrapper: policy-gated update admission for federated rounds with signed update checks and governance enforcement ([wrapper details](flower_security_wrapper/README.md)).
- Compliance Mapping: direct evidence links for HIPAA and GDPR controls ([Compliance Evidence](docs/beta/COMPLIANCE_EVIDENCE.md), [Beta Release Plan](docs/beta/BETA_RELEASE.md)).
- Interactive Dashboard: built-in 47-node global map simulation with click-through interactions across federated regions ([dashboard entry point](index.html)).
- DPIA Generator: built-in GDPR impact assessment workflow with validation and draft report generation ([dashboard section in app](app.js), [compliance evidence](docs/beta/COMPLIANCE_EVIDENCE.md)).

## Oncology Use Case

This platform supports multi-center oncology collaboration where hospitals can jointly improve models for early risk stratification, treatment response estimation, and trial cohort matching without sharing raw patient data.

In this workflow, each site trains locally, submits signed updates through policy-gated federated rounds, and receives governance-audited global improvements. The goal is faster translational learning across institutions while preserving privacy and compliance boundaries.

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
- WAL Ledger Integration:
  - CockroachDB/etcd-style append-only, hash-chained WAL controls in dashboard UI
  - Signed-ack integration mode, term/commit metadata, verification, export, and replay views
  - Linked backend implementation in `flower_security_wrapper/security_wrapper/wal_ledger.py`
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

## Contributing

See the contributor guide: [CONTRIBUTING.md](CONTRIBUTING.md)

### What you can do to contribute

- Add tests for governance contract decisions, rejection taxonomy, and adversarial scenarios.
- Improve attestation, nonce-store, and SIEM integration validation with more edge cases.
- Enhance dashboard UX with accessibility improvements and clearer risk/compliance states.
- Improve CI diagnostics and artifact quality checks for faster failure triage.
- Expand docs with architecture diagrams and incident/beta release runbooks.

### Ideas and current needs

- Security hardening:
  - Stronger poisoning detection heuristics and benchmark datasets.
  - More TPM attestation parsing and verification fixtures.
- Compliance automation:
  - Additional HIPAA/GDPR evidence mappings and export templates.
  - Better DPIA output quality and governance gate evidence capture.
- Developer experience:
  - More contributor-friendly examples for local simulation and testing.
  - Faster local verification scripts and make-style task shortcuts.

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
