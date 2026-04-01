#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "$0")/.." && pwd)"
ARTIFACT_DIR="$ROOT_DIR/docs/beta/artifacts"
mkdir -p "$ARTIFACT_DIR"

printf "[beta-artifacts] capturing release evidence\n"

date -u +"%Y-%m-%dT%H:%M:%SZ" > "$ARTIFACT_DIR/build_timestamp_utc.txt"

git -C "$ROOT_DIR" rev-parse HEAD > "$ARTIFACT_DIR/git_commit.txt"
git -C "$ROOT_DIR" status --short > "$ARTIFACT_DIR/git_status.txt"

cp "$ROOT_DIR/flower_security_wrapper/policy.example.json" "$ARTIFACT_DIR/policy.example.snapshot.json"
cp "$ROOT_DIR/flower_security_wrapper/policy.rare_disease.json" "$ARTIFACT_DIR/policy.rare_disease.snapshot.json"

printf "[beta-artifacts] done: %s\n" "$ARTIFACT_DIR"
