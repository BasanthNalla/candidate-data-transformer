from models.candidate import Candidate

from normalizers.link_normalizer import normalize_link
from normalizers.location_normalizer import normalize_location
from normalizers.skill_normalizer import normalize_skill
from normalizers.email_normalizer import normalize_email
from normalizers.phone_normalizer import normalize_phone
from normalizers.date_normalizer import normalize_date

class CandidateNormalizer:
    def normalize(self, candidate: Candidate) -> Candidate:
        candidate.emails = [
            normalize_email(email) for email in candidate.emails
        ]
        candidate.phones = [
            normalize_phone(phone) for phone in candidate.phones
        ]
        candidate.location = normalize_location(candidate.location)
        candidate.links = normalize_link(candidate.links)
        for skill in candidate.skills:
            skill.name = normalize_skill(skill.name)
        for education in candidate.education:
            education.end_year = normalize_date(education.end_year)
        for experience in candidate.experience:
            experience.start = normalize_date(experience.start)
            experience.end = normalize_date(experience.end)
        return candidate