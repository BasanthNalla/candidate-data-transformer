import re
import pdfplumber
import dateparser
import phonenumbers
from datetime import datetime

from models.candidate import Candidate
from models.skill import Skill
from models.location import Location
from models.link import Link
from utils.regex_patterns import EMAIL_REGEX, PHONE_REGEX, LINKEDIN_REGEX, GITHUB_REGEX, URL_REGEX, DATE_REGEX
from utils.skill_loader import SkillLoader
from utils.section_headers import SECTION_HEADERS
from utils.date_utils import split_date_range
from models.education import Education
from models.experience import Experience

class ResumeParser:
    RESUME_SOURCE = "Resume"
    
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
        experiences = self._extract_experience(sections.get("experience", ""))
        return Candidate(
            candidate_id="",
            full_name=self._extract_name(text),
            emails=self._extract_emails(text),
            phones=self._extract_phones(text),
            location=self._extract_location(text),
            links=self._extract_links(text),
            headline=self._extract_headline(text),
            years_experience=self._compute_years_experience(experiences),
            skills=self._extract_skills(sections.get("skills", "")),
            experience=experiences,
            education=self._extract_education(sections.get("education", "")),
            provenance=[],
            overall_confidence=0.0
        )
    
    def _extract_name(self, text: str) -> str:
        lines = [line.strip() for line in text.split("\n") if line.strip()]
        for line in lines:
            if re.search(EMAIL_REGEX, line): continue
            if re.search(PHONE_REGEX, line): continue
            if re.search(r"https?://", line): continue
            if line.isupper() and len(line.split()) == 1: continue
            if len(line.split()) >= 2:
                return line
        return ""
    
    def _extract_headline(self, text: str) -> str:
        name = self._extract_name(text)
        lines = [line.strip() for line in text.split("\n") if line.strip()]
        found_name = False
        for line in lines:
            if not found_name:
                if line == name:
                    found_name = True
                continue
            
            if re.search(EMAIL_REGEX, line): continue
            if re.search(PHONE_REGEX, line): continue
            if re.search(r"https?://", line): continue
            
            is_section_header = False
            for headers in SECTION_HEADERS.values():
                if line.lower() in headers:
                    is_section_header = True
                    break
            if is_section_header: continue
            
            if len(line) < 100:
                return line
        return None
        
    def _extract_location(self, text: str) -> Location:
        LOCATION_REGEX_3 = r"\b([A-Z][a-z]+(?:\s[A-Z][a-z]+)*),\s*([A-Z][a-z]+(?:\s[A-Z][a-z]+)*),\s*([A-Z][a-z]+(?:\s[A-Z][a-z]+)*)\b"
        LOCATION_REGEX_2 = r"\b([A-Z][a-z]+(?:\s[A-Z][a-z]+)*),\s*([A-Z][a-z]+(?:\s[A-Z][a-z]+)*)\b"
        KNOWN_COUNTRIES = {"india": "IN", "usa": "US", "united states": "US", "uk": "GB", "united kingdom": "GB"}
        
        lines = [line.strip() for line in text.split("\n") if line.strip()]
        for line in lines[:15]:
            match3 = re.search(LOCATION_REGEX_3, line)
            if match3:
                city, region, country = match3.groups()
                from normalizers.location_normalizer import _country_to_alpha2
                return Location(city=city, region=region, country=_country_to_alpha2(country))
                
            match2 = re.search(LOCATION_REGEX_2, line)
            if match2:
                city, region = match2.groups()
                country = None
                line_lower = line.lower()
                for c_name, c_code in KNOWN_COUNTRIES.items():
                    if c_name in line_lower:
                        country = c_code
                        break
                return Location(city=city, region=region, country=country)
        return Location()
    
    def _compute_years_experience(self, experiences: list[Experience]) -> float | None:
        if not experiences: return None
        total_months = 0
        for exp in experiences:
            if not exp.start: continue
            start_dt = dateparser.parse(exp.start)
            if not start_dt: continue
            if start_dt.tzinfo is not None:
                start_dt = start_dt.replace(tzinfo=None)
            if not exp.end or exp.end.lower() in ["present", "current", "ongoing"]:
                end_dt = datetime.now()
            else:
                end_dt = dateparser.parse(exp.end)
                if not end_dt: end_dt = datetime.now()
                elif end_dt.tzinfo is not None:
                    end_dt = end_dt.replace(tzinfo=None)
            
            months = (end_dt.year - start_dt.year) * 12 + end_dt.month - start_dt.month
            if months > 0:
                total_months += months
        if total_months == 0: return None
        return round(total_months / 12.0, 1)

    def _extract_emails(self, text: str) -> list[str]:
        emails = re.findall(EMAIL_REGEX, text)
        return list(set(emails))
    
    def _extract_phones(self, text: str) -> list[str]:
        phones = []
        for match in phonenumbers.PhoneNumberMatcher(text, "IN"):
            phones.append(match.raw_string)
        if not phones:
            phones = re.findall(PHONE_REGEX, text)
        return list(set(phones))
    
    def _extract_links(self, text: str) -> Link:
        linkedin = re.search(LINKEDIN_REGEX, text)
        github = re.search(GITHUB_REGEX, text)
        urls = re.findall(URL_REGEX, text)
        other = []
        for url in urls:
            if linkedin and linkedin.group() in url: continue
            if github and github.group() in url: continue
            other.append(url)
        return Link(
            linkedin=linkedin.group() if linkedin else None,
            github=github.group() if github else None,
            portfolio=other[0] if other else None,
            other=other[1:] if len(other) > 1 else []
        )
    
    def _extract_skills(self, section_text: str) -> list[Skill]:
        skills = []
        added = set()
        if not section_text.strip():
            return []
        tokens = re.split(r"[,•|\n;/]+", section_text)
        for token in tokens:
            token = token.strip()
            if not token: continue
            token_lower = token.lower()
            if token_lower in added: continue
            added.add(token_lower)
            if token_lower in self.known_skills:
                confidence = 0.95
            else:
                confidence = 0.7
            skills.append(Skill(name=token, confidence=confidence, sources=[self.RESUME_SOURCE]))
        return skills
    
    def _extract_sections(self, text: str) -> dict:
        sections = {}
        lines = [line.strip() for line in text.split("\n")]
        current_section = None
        for line in lines:
            lower = line.lower().rstrip(": \t")
            found = False
            for section_name, headers in SECTION_HEADERS.items():
                if lower in headers:
                    current_section = section_name
                    sections[current_section] = []
                    found = True
                    break
            if found: continue
            if current_section:
                sections[current_section].append(line)
        return {k: "\n".join(v) for k, v in sections.items()}
    
    def _extract_education(self, education_text: str) -> list[Education]:
        if not education_text.strip(): return []
        lines = [line.strip() for line in education_text.split("\n") if line.strip()]
        educations = []
        current_edu = {}
        
        for line in lines:
            year_match = re.search(r"\b(19|20)\d{2}\b", line)
            if year_match and "institution" in current_edu:
                try:
                    current_edu["end_year"] = int(year_match.group())
                except ValueError:
                    pass
                educations.append(Education(**current_edu))
                current_edu = {}
                continue
                
            if "institution" not in current_edu:
                current_edu["institution"] = line
            elif "degree" not in current_edu:
                current_edu["degree"] = line
            elif "field" not in current_edu:
                current_edu["field"] = line
                
        if current_edu and "institution" in current_edu:
            educations.append(Education(**current_edu))
            
        return educations
    
    def _extract_experience(self, experience_text: str) -> list[Experience]:
        if not experience_text.strip(): return []
        lines = [line.strip() for line in experience_text.split("\n") if line.strip()]
        experiences = []
        
        DATE_RANGE_PATTERN = re.compile(rf"({DATE_REGEX})\s*[-–—to]+\s*({DATE_REGEX})", re.IGNORECASE)
        
        i = 0
        while i < len(lines):
            company = lines[i]
            title = ""
            start = None
            end = None
            summary = []
            
            if i + 1 < len(lines) and not DATE_RANGE_PATTERN.search(lines[i+1]):
                title = lines[i+1]
                i += 2
            else:
                i += 1
                
            while i < len(lines):
                line = lines[i]
                if DATE_RANGE_PATTERN.search(line):
                    start, end = split_date_range(line)
                    i += 1
                    continue
                
                if len(summary) > 0 and not line.startswith(("-", "•", "*")) and line.istitle() and not line.endswith((".", ";", ",")):
                    break
                    
                summary.append(line)
                i += 1
                
            experiences.append(Experience(
                company=company,
                title=title,
                start=start,
                end=end,
                summary=" ".join(summary) if summary else None
            ))
            
        return experiences