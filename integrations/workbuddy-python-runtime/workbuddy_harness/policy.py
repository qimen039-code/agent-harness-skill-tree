from __future__ import annotations

import json
import os
from pathlib import Path
from typing import Any


DEFAULT_POLICY_PATH = Path(
    os.environ.get(
        "AGENT_MEMORY_LANE_POLICY",
        Path(__file__).resolve().parents[3] / "skills" / "embedded-harness" / "embedded_harness_policy.json",
    )
)


def _as_string_list(value: Any) -> list[str]:
    if value is None:
        return []
    if isinstance(value, list):
        return [str(item) for item in value if str(item)]
    return [str(value)]


def _merge_mapping_lists(policy: dict[str, Any], overlay: dict[str, Any], field: str) -> None:
    incoming = overlay.get(field)
    if not isinstance(incoming, dict):
        return
    target = policy.setdefault(field, {})
    if not isinstance(target, dict):
        target = {}
        policy[field] = target
    for lane, roots in incoming.items():
        merged = _as_string_list(target.get(str(lane))) + _as_string_list(roots)
        target[str(lane)] = list(dict.fromkeys(item for item in merged if item.strip()))


def _overlay_candidates(policy_path: Path, policy: dict[str, Any]) -> list[Path]:
    config = policy.get("local_project_lane_overlay", {})
    if isinstance(config, dict) and config.get("enabled") is False:
        return []
    env_var = str(config.get("env_var") or "CBH_PROJECT_LANES_FILE") if isinstance(config, dict) else "CBH_PROJECT_LANES_FILE"
    filename = (
        str(config.get("default_filename") or "embedded_harness_policy.local.json")
        if isinstance(config, dict)
        else "embedded_harness_policy.local.json"
    )
    candidates: list[Path] = []
    env_path = os.environ.get(env_var)
    if env_path:
        candidates.append(Path(env_path))
    candidates.append(policy_path.with_name(filename))
    return candidates


def _apply_local_project_lane_overlay(policy: dict[str, Any], policy_path: Path) -> dict[str, Any]:
    for candidate in _overlay_candidates(policy_path, policy):
        if not candidate.is_file():
            continue
        with candidate.open("r", encoding="utf-8-sig") as handle:
            overlay = json.load(handle)
        if not isinstance(overlay, dict):
            continue
        expected_schema = policy.get("local_project_lane_overlay", {}).get("schema") if isinstance(policy.get("local_project_lane_overlay"), dict) else None
        if expected_schema and overlay.get("schema") not in {expected_schema, None}:
            continue
        _merge_mapping_lists(policy, overlay, "project_lanes")
        _merge_mapping_lists(policy, overlay, "memory_roots")
        policy["_local_project_lane_overlay"] = {
            "loaded": True,
            "path": str(candidate),
            "rule": "machine-local project lane overlay; do not publish private roots",
        }
        break
    return policy


def load_policy(policy_path: str | os.PathLike[str] | None = None) -> dict[str, Any]:
    path = Path(policy_path) if policy_path else DEFAULT_POLICY_PATH
    with path.open("r", encoding="utf-8-sig") as handle:
        policy = json.load(handle)
    return _apply_local_project_lane_overlay(policy, path)
