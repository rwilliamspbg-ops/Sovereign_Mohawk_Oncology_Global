# Compliance Evidence (Beta)

## Control Mapping Summary

- Federated updates only (no raw PHI transfer): HIPAA 164.502, GDPR Art.5/25
- Differential privacy budget enforcement: HIPAA 164.514, GDPR Art.89
- Attestation and signed updates: HIPAA 164.312, GDPR Art.32
- Data minimization and payload controls: HIPAA minimum necessary, GDPR Art.5(1)(c)
- Audit and SIEM forwarding: HIPAA 164.312(b), GDPR Art.30/32

## Evidence Sources

- Unit and pentest tests in `flower_security_wrapper/tests`
- Runtime governance/slashing logs in JSONL audit stream
- Policy snapshots in `docs/beta/artifacts`
- CI build/test artifacts uploaded by GitHub Actions

## Beta Notes

- This beta demonstrates control enforcement and detection paths.
- Production deployment still requires formal key ceremony, secrets manager integration, and independent security assessment.
