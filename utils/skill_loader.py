from pathlib import Path
import os

class SkillLoader:
    def __init__(self, skill_file: str = None):
        if skill_file is None:
            BASE_DIR = Path(__file__).resolve().parent.parent
            self.skill_file = str(BASE_DIR / "resources" / "skills.txt")
        else:
            self.skill_file = skill_file

    def load_skills(self) -> set[str]:
        skills = set()
        try:
            with open(self.skill_file, "r", encoding="utf-8") as f:
                for line in f:
                    skill = line.strip()
                    if skill:
                        skills.add(skill.lower())
        except FileNotFoundError:
            print(f"[WARN] Skill file '{self.skill_file}' not found. Defaulting to empty skills list.")
        return skills