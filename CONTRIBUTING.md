# Contributing to Sovereign Mohawk Oncology Global

Thanks for contributing.

This repository contains:
- A browser-based operations dashboard (`index.html`, `styles.css`, `app.js`, `manifesto.html`)
- A Python Flower security wrapper (`flower_security_wrapper/`)
- CI/CD workflows under `.github/workflows/`

## Development Setup

```bash
cd flower_security_wrapper
python -m pip install --upgrade pip
pip install -r requirements-dev.txt
pip install -e .
```

## Validate Before PR

Run from the repository root unless noted.

1. Lint Python wrapper code:

```bash
ruff check flower_security_wrapper
```

2. Run tests and generate evidence artifacts:

```bash
pytest flower_security_wrapper/tests \
  --junitxml=flower_security_wrapper/junit.xml \
  --cov=flower_security_wrapper/security_wrapper \
  --cov-report=xml:flower_security_wrapper/coverage.xml
```

3. Build and validate package metadata:

```bash
cd flower_security_wrapper
python -m build
twine check dist/*
```

4. Optional: run frontend demo locally:

```bash
cd /workspaces/Sovereign_Mohawk_Oncology_Global
python3 -m http.server 8080
```

5. Optional: run demo with backend-fed HUD state:

```bash
cd /workspaces/Sovereign_Mohawk_Oncology_Global/flower_security_wrapper
python example_server.py --serve
```

## CI Workflows

- `.github/workflows/ci.yml`: lint, test, build, artifact upload
- `.github/workflows/pages.yml`: publish dashboard bundle to GitHub Pages (when enabled)
- `.github/workflows/beta-artifacts.yml`: capture beta release artifacts on `beta-*` tags or manual trigger
- `.github/workflows/release-drafter.yml`: maintain release drafts on `main`

## Scope Guidelines

- Keep changes focused. Avoid mixing unrelated frontend/backend/docs refactors in one PR.
- If you change policy semantics, include matching test updates in `flower_security_wrapper/tests/`.
- If you change HUD labels or behavior, update docs in `README.md`.
- Do not commit secrets, private keys, or PHI-like data.

## Branch and PR Guidance

- Branch naming:
  - `feat/<topic>`
  - `fix/<topic>`
  - `docs/<topic>`
  - `ci/<topic>`

- PR checklist:
  - Tests pass locally
  - Lint passes locally
  - Docs updated if behavior changed
  - CI artifacts still generated (`junit.xml`, `coverage.xml`, package build)

## License

By contributing, you agree your changes are provided under the repository license in `LICENSE`.
