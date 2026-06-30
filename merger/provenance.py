from models.provenance import Provenance

class ProvenanceTracker:

    def track(self, candidate, sources):
        candidate.provenance = []
        self._track_skills(candidate, sources)
        self._track_emails(candidate, sources)
        self._track_phones(candidate, sources)
        self._track_links(candidate, sources)
        self._track_experience(candidate, sources)
        self._track_education(candidate, sources)
        self._track_location(candidate, sources)
        self._track_scalar_fields(candidate, sources)
        return candidate
    
    def _track_skills(self, candidate, sources):
        for skill in candidate.skills:
            for source in set(skill.sources):
                candidate.provenance.append(
                    Provenance(
                        field=f"skills.{skill.name}",
                        value=skill.name,
                        source=source,
                        method="Matched" if len(set(skill.sources)) > 1 else "Parsed"
                    )
                )

    def _track_emails(self, candidate, sources):
        for email in candidate.emails:
            source_names = []
            for name, cand in sources:
                if email in (cand.emails or []):
                    source_names.append(name)
            for source_name in source_names:
                candidate.provenance.append(
                    Provenance(
                        field="email",
                        value=email,
                        source=source_name,
                        method="Matched" if len(source_names) > 1 else "Parsed"
                    )
                )

    def _track_phones(self, candidate, sources):
        for phone in candidate.phones:
            source_names = []
            for name, cand in sources:
                if phone in (cand.phones or []):
                    source_names.append(name)
            for source_name in source_names:
                candidate.provenance.append(
                    Provenance(
                        field="phone",
                        value=phone,
                        source=source_name,
                        method="Matched" if len(source_names) > 1 else "Parsed"
                    )
                )

    def _track_links(self, candidate, sources):
        links = candidate.links
        if not links: return

        def check_link(field, value):
            if not value: return
            source_names = []
            for name, cand in sources:
                if cand.links and getattr(cand.links, field) == value:
                    source_names.append(name)
            for source_name in source_names:
                candidate.provenance.append(Provenance(
                    field=field,
                    value=value,
                    source=source_name,
                    method="Matched" if len(source_names) > 1 else "Parsed"
                ))

        check_link("linkedin", links.linkedin)
        check_link("github", links.github)
        check_link("portfolio", links.portfolio)

        for other_link in (links.other or []):
            source_names = []
            for name, cand in sources:
                if cand.links and other_link in (cand.links.other or []):
                    source_names.append(name)
            for source_name in source_names:
                candidate.provenance.append(Provenance(
                    field="other_link",
                    value=other_link,
                    source=source_name,
                    method="Matched" if len(source_names) > 1 else "Parsed"
                ))

    def _track_experience(self, candidate, sources):
        for exp in candidate.experience:
            source_names = []
            for name, cand in sources:
                if any((c.company or "").lower() == (exp.company or "").lower() and 
                       (c.title or "").lower() == (exp.title or "").lower() 
                       for c in (cand.experience or [])):
                    source_names.append(name)
            for source_name in source_names:
                candidate.provenance.append(Provenance(
                    field=f"experience.{exp.company}",
                    value=f"{exp.company} - {exp.title}",
                    source=source_name,
                    method="Matched" if len(source_names) > 1 else "Parsed"
                ))

    def _track_education(self, candidate, sources):
        for edu in candidate.education:
            source_names = []
            for name, cand in sources:
                if any((r.institution or "").lower() == (edu.institution or "").lower() and 
                       (r.degree or "").lower() == (edu.degree or "").lower() 
                       for r in (cand.education or [])):
                    source_names.append(name)
            for source_name in source_names:
                candidate.provenance.append(Provenance(
                    field=f"education.{edu.institution}",
                    value=f"{edu.institution} - {edu.degree}",
                    source=source_name,
                    method="Matched" if len(source_names) > 1 else "Parsed"
                ))

    def _track_location(self, candidate, sources):
        if not candidate.location: return
        for field in ["city", "region", "country"]:
            value = getattr(candidate.location, field)
            if not value: continue
            
            source_names = []
            for name, cand in sources:
                if cand.location and (getattr(cand.location, field) or "").lower() == value.lower():
                    source_names.append(name)
                    
            for source_name in source_names:
                candidate.provenance.append(Provenance(
                    field=field,
                    value=value,
                    source=source_name,
                    method="Matched" if len(source_names) > 1 else "Parsed"
                ))
                
    def _track_scalar_fields(self, candidate, sources):
        for field in ["full_name", "headline", "years_experience", "candidate_id"]:
            value = getattr(candidate, field)
            if value is None or value == "": continue
            
            source_names = []
            for name, cand in sources:
                source_val = getattr(cand, field)
                if source_val == value:
                    source_names.append(name)
                    
            for source_name in source_names:
                candidate.provenance.append(Provenance(
                    field=field,
                    value=str(value),
                    source=source_name,
                    method="Matched" if len(source_names) > 1 else "Parsed"
                ))