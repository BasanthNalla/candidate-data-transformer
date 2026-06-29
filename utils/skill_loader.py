from pathlib import Path

class SkillLoader:
    def __init__(self, skill_file = "resources/skills.txt"):
        self.skill_file = Path(skill_file)

    def load_skills(self) -> set[str]:
        skills = set()
        with open(self.skill_file, "r", encoding="utf-8") as f:
            for line in f:
                skill = line.strip()
                if skill:
                    skills.add(skill.lower())
        return skills