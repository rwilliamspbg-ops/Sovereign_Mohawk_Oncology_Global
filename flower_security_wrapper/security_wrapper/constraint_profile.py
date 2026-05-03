from dataclasses import dataclass
from typing import Any, Dict, List, Sequence, cast


@dataclass(frozen=True)
class CompiledConstraintProfile:
    required_tags: List[str]
    forbidden_tags: List[str]


def compile_core_alignment_profile(metrics: Dict[str, Any]) -> CompiledConstraintProfile:
    """Compile v1 alignment constraints from runtime safety/governance signals."""
    required_tags: List[str] = ["categorical_alignment", "closure_verified"]
    forbidden_tags: List[str] = []

    if bool(metrics.get("data_deidentified", False)):
        required_tags.append("privacy_preserved")
    if bool(metrics.get("irb_approved", False)):
        required_tags.append("irb_validated")
    if bool(metrics.get("dpo_reviewed", False)):
        required_tags.append("dpo_reviewed")

    if not bool(metrics.get("attestation_ok", False)):
        forbidden_tags.append("hardware_untrusted")
    if not bool(metrics.get("signature_verified", False)):
        forbidden_tags.append("signature_unverified")
    if float(metrics.get("epsilon_spent", 999.0)) > float(
        metrics.get("dp_limit", 1.0)
    ):
        forbidden_tags.append("dp_out_of_budget")

    return CompiledConstraintProfile(
        required_tags=sorted(set(required_tags)),
        forbidden_tags=sorted(set(forbidden_tags)),
    )


def compile_profile(
    profile_name: str,
    metrics: Dict[str, Any],
) -> CompiledConstraintProfile:
    normalized = str(profile_name or "").strip().lower()
    if normalized in {"core_alignment_v1", "core-alignment-v1"}:
        return compile_core_alignment_profile(metrics)
    return CompiledConstraintProfile(required_tags=[], forbidden_tags=[])


def merge_tags(existing: Any, additions: Sequence[str]) -> List[str]:
    base: List[str]
    if isinstance(existing, list):
        base = []
        existing_list = cast(List[Any], existing)
        for item in existing_list:
            text = str(item).strip()
            if text:
                base.append(text)
    elif isinstance(existing, str):
        base = [item.strip() for item in existing.split(",") if item.strip()]
    else:
        base = []

    merged = set(base)
    merged.update(str(item).strip() for item in additions if str(item).strip())
    return sorted(merged)
