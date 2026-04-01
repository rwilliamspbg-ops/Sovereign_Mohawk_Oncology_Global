# Beta Release Plan

## Scope

- Dashboard demo deployment via GitHub Pages
- Python package build for `flower_security_wrapper`
- CI quality gates for tests, lint, and packaging integrity
- Security and compliance evidence capture for beta artifacts

## CI Workflows

- `ci.yml`: unit tests, pentest simulations, lint, package build
- `pages.yml`: publishes dashboard (`index.html`, `styles.css`, `app.js`) to GitHub Pages
- `beta-artifacts.yml`: captures and uploads release evidence bundle

## Beta Artifacts

- Test results (`junit.xml`)
- Coverage report (`coverage.xml`)
- Wheel and sdist (`dist/`)
- Policy snapshots and repository metadata (`docs/beta/artifacts/`)

## Suggested Additional Artifacts

- Signed SBOM for package dependencies
- Exported SIEM sample alert events from staging
- Adversarial exercise output transcript and pass/fail rubric
- Cryptographic key-rotation evidence (redacted)
- Governance/slashing event summary dashboard snapshot

## Exit Criteria

- CI green on `main`
- Package built and uploaded as workflow artifact
- Pages deployment successful
- Compliance evidence checklist completed
