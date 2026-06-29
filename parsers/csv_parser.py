import pandas as pd
from models.candidate import Candidate
from models.skill import Skill
from models.location import Location
from models.link import Link

class CSVParser:
    CSV_SOURCE = "Recruiter CSV"
    CSV_SKILL_CONFIDENCE = 0.9
    def __init__(self, csv_path):
        self.csv_path = csv_path

    def parse(self) -> list[Candidate]:
        df = pd.read_csv(self.csv_path)
        candidates = []
        for _, row in df.iterrows():
            candidate = self._parse_candidate(row)
            candidates.append(candidate)
        return candidates

    def _parse_candidate(self, row) -> Candidate:
        return Candidate(
            candidate_id = self._get_value(row, "candidate_id"),
            full_name = self._get_value(row, "full_name"),
            emails = self._parse_email(self._get_value(row, "email")),
            phones = self._parse_phone(self._get_value(row, "phone")),
            location = self._parse_location(row),
            links = self._parse_links(row),
            headline = self._get_value(row, "headline"),
            years_experience = self._parse_years(self._get_value(row, "years_experience")),
            skills = self._parse_skills(self._get_value(row, "skills")),
            experience = [],
            education = [],
            provenance = [],
            overall_confidence = self.CSV_SKILL_CONFIDENCE
        )

    def _parse_skills(self, skills: str) -> list[Skill]:
        if not skills:
            return []
        skill_list = []
        for skill in skills.split(","):
            skill = skill.strip()
            if skill:
                skill_list.append(Skill(name=skill, confidence=self.CSV_SKILL_CONFIDENCE, sources=[self.CSV_SOURCE]))
        return skill_list

    def _parse_location(self, row) -> Location:
        return Location(
            city=self._get_value(row, "city"),
            region=self._get_value(row, "region"),
            country=self._get_value(row, "country")
        )

    def _parse_links(self, row) -> list[Link]:
        return Link(
                linkedin=self._get_value(row, "linkedin"),
                github=self._get_value(row, "github"),
                portfolio=self._get_value(row, "portfolio"),
                other=[]
            )
    
    def _parse_email(self, email: str) -> list[str]:
        if not email:
            return []
        return [email.strip()]
    
    def _parse_phone(self, phone: str) -> list[str]:
        if not phone:
            return []
        return [phone.strip()]
    
    def _parse_years(self, years):
        if pd.isna(years):
            return None
        try:
            return int(years)
        except:
            return None
        
    def _get_value(self, row, column):
        value = row.get(column)
        if pd.isna(value):
            return None
        return str(value).strip()
    
