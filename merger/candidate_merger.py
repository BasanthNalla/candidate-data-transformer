from copy import deepcopy

class CandidateMerger:
    def __init__(self, sources):
        """sources is a list of tuples: (source_name, candidate)"""
        # Filter out None candidates
        self.sources = [(name, cand) for name, cand in sources if cand is not None]

    def _merge_unique(self, key_func, extract_list_func):
        merged = []
        seen = set()
        for _, candidate in self.sources:
            items = extract_list_func(candidate)
            for item in items or []:
                try:
                    key = key_func(item)
                except Exception:
                    continue
                if key not in seen:
                    merged.append(deepcopy(item))
                    seen.add(key)
        return merged
    
    def _pick(self, extract_func):
        for _, candidate in self.sources:
            val = extract_func(candidate)
            if val is not None and val != "":
                return deepcopy(val)
        return None
    
    def merge(self):
        if not self.sources:
            return None
            
        # Initialize with a base candidate
        merged = deepcopy(self.sources[0][1])
        
        merged.candidate_id = self._pick(lambda c: c.candidate_id)
        merged.full_name = self._pick(lambda c: c.full_name)
        merged.emails = self._merge_emails()
        merged.phones = self._merge_phones()
        merged.location = self._merge_location()
        merged.links = self._merge_links()
        merged.headline = self._pick(lambda c: c.headline)
        merged.years_experience = self._pick(lambda c: c.years_experience)
        merged.skills = self._merge_skills()
        merged.education = self._merge_education()
        merged.experience = self._merge_experience()
        merged.overall_confidence = 0.0
        merged.provenance = []
        return merged
    
    def _merge_skills(self):
        skill_map = {}
        for source_name, candidate in self.sources:
            for skill in candidate.skills or []:
                key = (skill.name or "").lower()
                if key in skill_map:
                    skill_map[key].sources = list(set(skill_map[key].sources + skill.sources))
                else:
                    skill_map[key] = deepcopy(skill)
        return list(skill_map.values())
    
    def _merge_links(self):
        links = deepcopy(self.sources[0][1].links) if self.sources[0][1].links else None
        if not links:
            from models.link import Link
            links = Link()
            
        for _, candidate in self.sources:
            c_links = candidate.links
            if not c_links: continue
            
            if not links.linkedin: links.linkedin = c_links.linkedin
            if not links.github: links.github = c_links.github
            if not links.portfolio: links.portfolio = c_links.portfolio
            
            links.other = list(dict.fromkeys((links.other or []) + (c_links.other or [])))
            
        return links
    
    def _merge_experience(self):
        return self._merge_unique(
            lambda e: ((e.company or "").strip().lower(), (e.title or "").strip().lower()),
            lambda c: c.experience
        )
    
    def _merge_education(self):
        return self._merge_unique(
            lambda e: ((e.institution or "").strip().lower(), (e.degree or "").strip().lower()),
            lambda c: c.education
        )
    
    def _merge_emails(self):
        emails = set()
        for _, candidate in self.sources:
            for email in (candidate.emails or []):
                if email:
                    emails.add(email)
        return sorted(emails)
    
    def _merge_phones(self):
        phones = set()
        for _, candidate in self.sources:
            for phone in (candidate.phones or []):
                if phone:
                    phones.add(phone)
        return sorted(phones)
    
    def _merge_location(self):
        loc = deepcopy(self.sources[0][1].location) if self.sources[0][1].location else None
        if not loc:
            from models.location import Location
            loc = Location()
            
        for _, candidate in self.sources:
            c_loc = candidate.location
            if not c_loc: continue
            
            if not loc.city: loc.city = c_loc.city
            if not loc.region: loc.region = c_loc.region
            if not loc.country: loc.country = c_loc.country
            
        return loc
