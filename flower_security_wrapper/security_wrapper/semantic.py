import json
from typing import Any, Dict, Iterable, List, Optional, Set, cast


RECOMMENDED_SEMANTIC_FIELDS = [
    "entity",
    "relation",
    "role",
    "confidence",
    "provenance",
]


def parse_semantic_fragment(raw_fragment: Any) -> Optional[Dict[str, Any]]:
    if isinstance(raw_fragment, dict):
        return cast(Dict[str, Any], raw_fragment)
    if isinstance(raw_fragment, str):
        try:
            parsed = json.loads(raw_fragment)
            if isinstance(parsed, dict):
                return cast(Dict[str, Any], parsed)
        except json.JSONDecodeError:
            return None
    return None


def is_valid_semantic_fragment(
    fragment: Dict[str, Any],
    required_fields: Iterable[str],
    min_confidence: float,
) -> bool:
    for field in required_fields:
        if field not in fragment:
            return False

    try:
        confidence = float(fragment.get("confidence", 0.0))
    except (TypeError, ValueError):
        return False

    if confidence < min_confidence:
        return False

    provenance = str(fragment.get("provenance", "")).strip()
    if not provenance:
        return False

    return True


def has_constraint_closure(
    raw_tags: Any,
    required_tags: Iterable[str],
    forbidden_tags: Iterable[str],
) -> bool:
    tags: List[str]
    if isinstance(raw_tags, str):
        tags = [item.strip() for item in raw_tags.split(",") if item.strip()]
    elif isinstance(raw_tags, list):
        tags = []
        raw_tag_list = cast(List[Any], raw_tags)
        for item in raw_tag_list:
            text = str(item).strip()
            if text:
                tags.append(text)
    else:
        tags = []

    tag_set: Set[str] = {tag.lower() for tag in tags}
    required_set = {str(tag).strip().lower() for tag in required_tags if str(tag).strip()}
    forbidden_set = {
        str(tag).strip().lower() for tag in forbidden_tags if str(tag).strip()
    }

    if required_set and not required_set.issubset(tag_set):
        return False

    if forbidden_set.intersection(tag_set):
        return False

    return True
