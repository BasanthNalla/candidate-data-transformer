import re
import pdfplumber

from models.candidate import Candidate
from models.skill import Skill
from models.location import Location
from models.link import Link
from utils.regex_patterns import *
from utils.skill_loader import SkillLoader
from utils.section_headers import SECTION_HEADERS
from models.education import Education
from models.experience import Experience

class ResumeParser:
    RESUME_SOURCE = "Resume"
    RESUME_SKILL_CONFIDENCE = 0.95
    
    def __init__(self, resume_path: str):
        self.resume_path = resume_path
        self.skill_loader = SkillLoader()
        self.known_skills = self.skill_loader.load_skills()
    
    def parse(self) -> Candidate:
        text = self._extract_text()
        sections = self._extract_sections(text)
        return self._parse_candidate(text, sections)
    
    def _extract_text(self) -> str:
        text = ""
        with pdfplumber.open(self.resume_path) as pdf:
            for page in pdf.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text + "\n"

        return text
    
    def _parse_candidate(self, text, sections) -> Candidate:
        return Candidate(
            candidate_id="",
            full_name=self._extract_name(text),
            emails=self._extract_emails(text),
            phones=self._extract_phones(text),
            location=Location(),
            links=self._extract_links(text),
            headline=self._extract_headline(text),
            years_experience=None,
            skills=self._extract_skills(
                sections.get("skills", "")
            ),
            experience=self._extract_experience(
                sections.get("experience", "")
            ),
            education=self._extract_education(
                sections.get("education", "")
            ),
            provenance=[],
            overall_confidence=0.95
        )
    
    def _extract_name(self, text: str) -> str:
        lines=[line.strip() for line in text.split("\n") if line.strip()]
        if lines:
            return lines[0]
        return ""
    
    def _extract_emails(self, text: str) -> list[str]:
        emails = re.findall(EMAIL_REGEX, text)
        return list(set(emails))
    
    def _extract_phones(self, text: str) -> list[str]:
        phones = re.findall(PHONE_REGEX, text)
        return list(set(phones))
    
    def _extract_headline(self, text: str) -> str:
        lines = [line.strip() for line in text.split("\n") if line.strip()]
        if len(lines) >= 2:
            return lines[1]
        return None
    
    def _extract_links(self, text: str) -> Link:
        linkedin = re.search(LINKEDIN_REGEX, text)
        github = re.search(GITHUB_REGEX, text)
        urls = re.findall(URL_REGEX, text)
        other = []
        for url in urls:
            if linkedin and url == linkedin.group():
                continue
            if github and url == github.group():
                continue
            other.append(url)
        return Link(
            linkedin=linkedin.group() if linkedin else None,
            github=github.group() if github else None,
            portfolio=other[0] if other else None,
            other=other[1:] if len(other) > 1 else []
        )
    
    def _extract_skills(self, text: str) -> list[Skill]:
        skills = []
        added = set()
        section_match = re.search(SKILLS_SECTION_REGEX, text)
        if not section_match:
            return []
        skills_text = section_match.group(1)
        tokens = re.split(r"[,•|\n;/]+", skills_text)
        for token in tokens:
            token = token.strip()
            if not token:
                continue
            token_lower = token.lower()
            if token_lower in added:
                continue
            added.add(token_lower)
            if token_lower in self.known_skills:
                confidence = 0.95
            else:
                confidence = 0.7
            skills.append(
                Skill(
                    name=token,
                    confidence=confidence,
                    sources=[self.RESUME_SOURCE]
                )
            )
        return skills
    
    def _extract_sections(self, text: str) -> dict:
        sections = {}
        lines = [line.strip() for line in text.split("\n")]
        current_section = None
        for line in lines:
            lower = line.lower()
            found = False
            for section_name, headers in SECTION_HEADERS.items():
                if lower in headers:
                    current_section = section_name
                    sections[current_section] = []
                    found = True
                    break
            if found:
                continue
            if current_section:
                sections[current_section].append(line)
        return {
            key: "\n".join(value)
            for key, value in sections.items()
        }
    
    def _extract_education(self, education_text: str) -> list[Education]:
        if not education_text.strip():
            return []
        lines = [
            line.strip()
            for line in education_text.split("\n")
            if line.strip()
        ]
        institution = ""
        degree = ""
        field = None
        end_year = None
        if len(lines) >= 1:
            institution = lines[0]
        if len(lines) >= 2:
            degree = lines[1]
        if len(lines) >= 3:
            field = lines[2]
        dates = re.findall(DATE_REGEX, education_text)
        if len(dates)>=2:
            end_year = dates[1]
        return [
            Education(
                institution=institution,
                degree=degree,
                field=field,
                end_year=end_year
            )
        ]
    
    def _extract_experience(self, experience_text: str) -> list[Experience]:
        if not experience_text.strip():
            return []
        lines = [
            line.strip()
            for line in experience_text.split("\n")
            if line.strip()
        ]
        company = ""
        title = ""
        start = None
        end = None
        summary = None
        if len(lines) >= 1:
            company = lines[0]
        if len(lines) >= 2:
            title = lines[1]
        dates = re.findall(DATE_REGEX, experience_text)
        if len(dates) >= 1:
            start = dates[0]
        if len(dates) >= 2:
            end = dates[1]
        if len(lines) >= 4:
            summary = " ".join(lines[3:])
        return [
            Experience(
                company=company,
                title=title,
                start=start,
                end=end,
                summary=summary
            )
        ]