from __future__ import annotations

import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / "integrations" / "doubao-native-skill" / "claim-boundary-harness"


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def parse_frontmatter(text: str) -> dict[str, str]:
    match = re.match(r"^---\n(.*?)\n---\n", text, re.S)
    assert match, "missing YAML frontmatter"
    fields: dict[str, str] = {}
    for line in match.group(1).splitlines():
        key, value = line.split(":", 1)
        fields[key.strip()] = value.strip().strip('"')
    return fields


def test_doubao_native_skill_has_minimal_trigger_surface() -> None:
    skill_md = SKILL / "SKILL.md"
    assert skill_md.is_file()
    fields = parse_frontmatter(read_text(skill_md))

    assert fields["name"] == "claim-boundary-harness"
    assert set(fields) == {"name", "description"}
    assert "声明边界" in fields["description"]
    assert "风险判断" in fields["description"]
    assert len(fields["description"]) <= 250


def test_doubao_native_skill_uses_progressive_disclosure() -> None:
    required = [
        "references/activation.md",
        "references/host-adapter.md",
        "references/routing-and-boundaries.md",
        "references/memory-ledger.md",
        "references/output-contract.md",
        "agents/openai.yaml",
        "scripts/init_memory.py",
        "scripts/derive_claims.py",
        "scripts/lint_claims.py",
        "scripts/repair_claims.py",
        "templates/facts.json",
        "templates/hypotheses.json",
    ]
    for relative in required:
        assert (SKILL / relative).is_file(), relative

    forbidden = {"README.md", "INSTALLATION_GUIDE.md", "QUICK_REFERENCE.md", "CHANGELOG.md"}
    present = {path.name for path in SKILL.rglob("*") if path.is_file()}
    assert not (present & forbidden)


def test_doubao_native_skill_is_not_bound_to_old_chat_demo() -> None:
    combined = "\n".join(read_text(path) for path in SKILL.rglob("*") if path.is_file())

    assert "2026-06-25\\new-chat\\claim-boundary-demo" not in combined
    assert "AppData\\Local\\Doubao\\Application" in combined
    assert ".doubao\\agent_mode\\workspace\\.skills" in combined
    assert "sync_skill_folder_to_cloud_disk" in combined
    assert "runtime-expanded only" in combined


def test_doubao_native_scripts_avoid_emoji_stdout_markers() -> None:
    for path in (SKILL / "scripts").glob("*.py"):
        text = read_text(path)
        for line in text.splitlines():
            if "print(" in line:
                assert not re.search(r"[✅❌⚠🔍🔧📋📊📈🔄💾]", line), f"{path.name}: {line}"
