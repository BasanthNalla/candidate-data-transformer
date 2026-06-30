def normalize_skill(skill: str) -> str:
    if not skill:
        return ""
    return skill.strip().title()