from copy import deepcopy

class CandidateMerger:
    def __init__(self, resume_candidate, csv_candidate):
        self.resume = resume_candidate
        self.csv = csv_candidate

    def _merge_unique(self, resume_list, csv_list, key_func):
        merged = []
        seen = set()
        for item in resume_list or []:
            try:
                key = key_func(item)
            except Exception:
                continue
            if key not in seen:
                merged.append(deepcopy(item))
                seen.add(key)
        for item in csv_list or []:
            try:
                key = key_func(item)
            except Exception:
                continue
            if key not in seen:
                merged.append(deepcopy(item))
                seen.add(key)
        return merged
    
    def _pick(self, resume_value, csv_value):
        if resume_value:
            return deepcopy(resume_value)
        return deepcopy(csv_value) if csv_value else None
    
    def merge(self):
        merged = deepcopy(self.resume if self.resume else self.csv)
        merged.candidate_id = self._pick(
            self.resume.candidate_id,
            self.csv.candidate_id
        )
        merged.full_name = self._pick(
            self.resume.full_name,
            self.csv.full_name
        )
        merged.emails = self._merge_emails()
        merged.phones = self._merge_phones()
        merged.location = self._merge_location()
        merged.links = self._merge_links()
        merged.headline = self._pick(
            self.resume.headline,
            self.csv.headline
        )
        merged.years_experience = self._pick(
            self.resume.years_experience,
            self.csv.years_experience
        )
        merged.skills = self._merge_skills()
        merged.education = self._merge_education()
        merged.experience = self._merge_experience()
        merged.overall_confidence = 0.0
        merged.provenance = []
        return merged
    
    def _merge_skills(self):
        return self._merge_unique(
            self.resume.skills,
            self.csv.skills,
            lambda s: (s.name or "").lower()
        )
    
    def _merge_links(self):
        if self.resume.links:
            links = deepcopy(self.resume.links)
        else:
            links = deepcopy(self.csv.links)
        if not links.linkedin:
            links.linkedin = self.csv.links.linkedin
        if not links.github:
            links.github = self.csv.links.github
        if not links.portfolio:
            links.portfolio = self.csv.links.portfolio
        links.other = list(
            dict.fromkeys(
                (self.resume.links.other or []) + (self.csv.links.other or [])
            )
        )
        return links
    
    def _merge_experience(self):
        return self._merge_unique(
            self.resume.experience,
            self.csv.experience,
            lambda e: (
                (e.company or "").strip().lower(),
                (e.title or "").strip().lower()
            )
        )
    
    def _merge_education(self):
        return self._merge_unique(
            self.resume.education,
            self.csv.education,
            lambda e: (
                (e.institution or "").strip().lower(),
                (e.degree or "").strip().lower()
            )
        )
    
    def _merge_emails(self):
        emails = set()
        for email in (self.resume.emails or []):
            if email:
                emails.add(email)
        for email in (self.csv.emails or []):
            if email:
                emails.add(email)
        return sorted(emails)
    
    def _merge_phones(self):
        phones = set()
        for phone in (self.resume.phones or []):
            if phone:
                phones.add(phone)
        for phone in (self.csv.phones or []):
            if phone:
                phones.add(phone)
        return sorted(phones)
    
    def _merge_location(self):
        if self.resume.location:
            location = deepcopy(self.resume.location)
        else:
            location = deepcopy(self.csv.location)
        if not location.city:
            location.city = self.csv.location.city
        if not location.region:
            location.region = self.csv.location.region
        if not location.country:
            location.country = self.csv.location.country
        return location
    
