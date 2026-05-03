# Release Readiness Checklist

## Purpose

This checklist defines go/no-go release criteria for the Verified Semantic Runtime rollout in the Flower security wrapper.

## Scope

- Semantic runtime enforcement (semantic fragment validation + constraint closure)
- Replay determinism and benchmark p95 SLO quality gates
- Strict rare-disease policy integrity and evidence artifacts

## Gate Matrix

| Gate | Source | Pass Condition | Blocking Condition |
| --- | --- | --- | --- |
| Lint | `.github/workflows/ci.yml` (`ruff check`) | No lint errors | Any lint failure |
| Core Tests | `.github/workflows/ci.yml` (`pytest flower_security_wrapper/tests`) | Test suite passes with coverage artifact output | Any test failure |
| Semantic Replay Determinism | `.github/workflows/ci.yml` (`test_semantic_replay.py`) | Deterministic replay outcomes across repeated runs | Replay nondeterminism or assertion failure |
| Benchmark p95 SLO Regression | `.github/workflows/ci.yml` (`test_wrapper_benchmarks.py`) | p95 behavior asserts both violation and non-violation paths correctly | Missing/incorrect p95 SLO behavior |
| Package Integrity | `.github/workflows/ci.yml` (`python -m build` + `twine check`) | Wheel/sdist build and metadata checks pass | Build or metadata check failure |

## Runtime Policy Readiness

All must be true in strict profile (`policy.rare_disease.json`):

- `enable_semantic_validation` is `true`
- `require_constraint_closure` is `true`
- `constraint_compiler_profile` is set to `core_alignment_v1`
- `benchmark_client_eval_p95_budget_ms` is set to a non-zero budget
- `required_metrics` includes `semantic_fragment` and `alignment_tags`
- `slash_amounts` includes explicit penalties for:
  - `SEMANTIC_FRAGMENT_INVALID`
  - `CONSTRAINT_CLOSURE_FAILED`

## Required Evidence Artifacts

Release package must include:

- `flower_security_wrapper/junit.xml`
- `flower_security_wrapper/coverage.xml`
- `flower_security_wrapper/dist/*`
- Policy snapshot for strict profile
- Git metadata (`commit`, `status`) in artifact bundle

## Pre-Release Verification Commands

Run from repository root:

```bash
cd flower_security_wrapper
python -m pip install -e .
pytest tests/test_semantic_replay.py tests/test_wrapper_benchmarks.py tests/test_policy.py -q
pytest -q
```

## Go/No-Go Decision Rules

- GO:
  - All CI gates pass on `main`.
  - All required artifacts are present and valid.
  - Strict policy fields match runtime requirements.
- NO-GO:
  - Any blocking condition from Gate Matrix occurs.
  - Missing semantic runtime fields or missing semantic slashing penalties.
  - p95 SLO regression tests fail.

## Rollback Trigger Conditions

Immediately stop release and revert to prior stable tag if any are observed in staging or canary:

- Replay outcomes diverge for identical input/event streams.
- Unexpected increase in semantic rejection false positives.
- Repeated `round_benchmark_slo_violation` events above accepted operational threshold.
- Attestation/signature validation regressions for known-good clients.

## Owner Sign-Off

- Security Engineering:
- ML Platform:
- Compliance/Governance:
- Release Manager:
- Date:
