# Contributing to Sovereign_Mohawk_Oncology_Global

Thank you for helping improve this project.

## Ways to Contribute

- Report bugs with clear reproduction steps
- Propose features for the dashboard and security wrapper
- Improve test coverage and CI reliability
- Improve docs for compliance, deployment, and onboarding
- Help validate security controls and governance checks

## Local Setup

### Dashboard (static app)

```bash
cd /workspaces/Sovereign_Mohawk_Oncology_Global
python3 -m http.server 8080
```

Open `http://localhost:8080`.

### Python security wrapper

```bash
cd /workspaces/Sovereign_Mohawk_Oncology_Global/flower_security_wrapper
python -m pip install --upgrade pip
pip install -r requirements-dev.txt
pip install -e .
```

## Run Quality Checks

```bash
cd /workspaces/Sovereign_Mohawk_Oncology_Global
ruff check flower_security_wrapper
pytest flower_security_wrapper/tests
```

Optional package validation:

```bash
cd /workspaces/Sovereign_Mohawk_Oncology_Global/flower_security_wrapper
python -m build
twine check dist/*
```

## Contribution Workflow

1. Create a branch from `main`.
2. Keep changes scoped to one feature/fix.
3. Add or update tests for behavior changes.
4. Update docs when user-facing behavior changes.
5. Open a PR with a clear summary and validation notes.

## Pull Request Checklist

- [ ] Code builds and tests pass locally
- [ ] Security-relevant changes include tests
- [ ] Compliance mappings/docs updated where applicable
- [ ] README/CONTRIBUTING updated for any new workflows

## High-Impact Areas (Current Needs)

- Security hardening:
  - Expand attestation validation scenarios
  - Improve poisoning/anomaly detection robustness
  - Add more SIEM integration fixtures and tests
- Reliability:
  - Add integration tests around governance contract decisions
  - Improve CI matrix coverage and failure diagnostics
- Frontend dashboard:
  - Add richer data simulations and edge-case states
  - Improve accessibility and keyboard navigation
- Documentation:
  - Add architecture diagrams for policy and slashing flows
  - Improve runbooks for beta release and incident response

## Reporting Security Issues

If you identify a potential vulnerability, avoid posting sensitive details in a public issue. Open a minimal issue and request a private disclosure channel.

## Code Style

- Keep changes minimal and focused
- Preserve existing naming/style conventions
- Prefer explicit tests over implicit assumptions
- Keep comments short and useful
