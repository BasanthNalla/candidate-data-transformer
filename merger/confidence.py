from utils.confidence_config import *

class ConfidenceCalculator:

    def calculate(self, candidate):
        skills_conf = self._calculate_skill_confidence(candidate)
        exp_conf = self._calculate_experience_confidence(candidate)
        edu_conf = self._calculate_education_confidence(candidate)
        email_conf = self._calculate_email_confidence(candidate)
        phone_conf = self._calculate_phone_confidence(candidate)
        links_conf = self._calculate_links_confidence(candidate)
        location_conf = self._calculate_location_confidence(candidate)
        overall = self._calculate_overall_confidence(
            skills_conf,
            exp_conf,
            edu_conf,
            email_conf,
            phone_conf,
            links_conf,
            location_conf
        )
        candidate.overall_confidence = overall
        return candidate
    
    def _calculate_skill_confidence(self, candidate):
        if not candidate.skills:
            return 0
        total = 0
        for skill in candidate.skills:
            source_count = len(set(skill.sources or []))
            if source_count>=2:
                skill.confidence = SKILL_MULTI_SOURCE
            elif source_count==1:
                skill.confidence = SKILL_SINGLE_SOURCE
            else:
                skill.confidence = SKILL_INFERRED
            total += skill.confidence
        return total/len(candidate.skills)
    
    def _calculate_experience_confidence(self, candidate):
        if not candidate.experience:
            return 0
        total = 0
        for exp in candidate.experience:
            has_company = bool(exp.company and exp.company.strip())
            has_title = bool(exp.title and exp.title.strip())
            if has_company and has_title:
                total += EXPERIENCE_COMPLETE
            elif has_company:
                total += EXPERIENCE_COMPANY_ONLY
            elif has_title:
                total += EXPERIENCE_TITLE_ONLY
            else:
                total += EXPERIENCE_PARTIAL
        return total/len(candidate.experience)
    
    def _calculate_education_confidence(self, candidate):
        if not candidate.education:
            return 0
        total = 0
        for edu in candidate.education:
            has_institution = bool(edu.institution and edu.institution.strip())
            has_degree = bool(edu.degree and edu.degree.strip())
            if has_institution and has_degree:
                total += EDUCATION_COMPLETE
            elif has_institution:
                total += EDUCATION_INSTITUTION_ONLY
            elif has_degree:
                total += EDUCATION_DEGREE_ONLY
            else:
                total += EDUCATION_PARTIAL
        return total/len(candidate.education)
    
    def _calculate_email_confidence(self, candidate):
        if candidate.emails:
            return EMAIL_PRESENT
        return EMAIL_ABSENT
    
    def _calculate_phone_confidence(self, candidate):
        if candidate.phones:
            return PHONE_PRESENT
        return PHONE_ABSENT
    
    def _calculate_links_confidence(self, candidate):
        links = candidate.links
        if not links:
            return 0
        score = 0
        if links.linkedin:
            score += LINKEDIN_SCORE
        if links.github:
            score += GITHUB_SCORE
        if links.portfolio:
            score += PORTFOLIO_SCORE
        score += min(len(links.other or []), 2)*OTHER_LINK_SCORE
        return min(score, 1.0)
    
    def _calculate_location_confidence(self, candidate):
        location = candidate.location
        if not location:
            return LOCATION_UNKNOWN
        city = bool(location.city)
        region = bool(location.region)
        country = bool(location.country)
        if city and region and country:
            return LOCATION_COMPLETE
        elif region and country:
            return LOCATION_NO_CITY
        elif country:
            return LOCATION_COUNTRY_ONLY
        return LOCATION_UNKNOWN
    
    def _calculate_overall_confidence(
            self,
            skills_conf,
            exp_conf,
            edu_conf,
            email_conf,
            phone_conf,
            links_conf,
            location_conf
    ):
        overall = (
            skills_conf*WEIGHTS["skills"] +
            exp_conf*WEIGHTS["experience"] +
            edu_conf*WEIGHTS["education"] +
            email_conf*WEIGHTS["email"] +
            phone_conf*WEIGHTS["phone"] +
            links_conf*WEIGHTS["links"] +
            location_conf*WEIGHTS["location"]
        )
        overall = max(min(overall, 1.0), 0.0)
        return round(overall, 2)