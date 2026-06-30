import json
from pathlib import Path

SKILL_ALIASES = {}

def _load_aliases():
    global SKILL_ALIASES
    if not SKILL_ALIASES:
        base_dir = Path(__file__).resolve().parent.parent
        alias_file = base_dir / "resources" / "skill_aliases.json"
        if alias_file.exists():
            with open(alias_file, "r", encoding="utf-8") as f:
                SKILL_ALIASES = json.load(f)

def normalize_skill(skill: str) -> str:
    if not skill:
        return ""
    _load_aliases()
    lower_skill = skill.strip().lower()
    return SKILL_ALIASES.get(lower_skill, skill.strip().title())