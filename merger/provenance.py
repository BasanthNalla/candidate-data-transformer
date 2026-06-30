from models.provenance import Provenance

class ProvenanceTracker:

    def track(self, candidate, resume_candidate, csv_candidate):
        candidate.provenance = []
        self._track_skills(candidate, resume_candidate, csv_candidate)
        self._track_emails(candidate, resume_candidate, csv_candidate)
        self._track_phones(candidate, resume_candidate, csv_candidate)
        self._track_links(candidate, resume_candidate, csv_candidate)
        self._track_experience(candidate, resume_candidate, csv_candidate)
        self._track_education(candidate, resume_candidate, csv_candidate)
        self._track_location(candidate, resume_candidate, csv_candidate)
        return candidate
    
    def _track_skills(self, candidate, resume_candidate, csv_candidate):
        for skill in candidate.skills:
            for source in set(skill.sources):
                candidate.provenance.append(
                    Provenance(
                        field = "skills",
                        value = skill.name,
                        source = source,
                        method = "Matched" if len(set(skill.sources))>1 else "Parsed"
                    )
                )

    def _track_emails(self, candidate, resume_candidate, csv_candidate):
        for email in candidate.emails:
            resume_found = email in (resume_candidate.emails or [])
            csv_found = email in (csv_candidate.emails or [])
            if resume_found:
                candidate.provenance.append(
                    Provenance(
                        field = "email",
                        value = email,
                        source = "Resume",
                        method = "Matched" if csv_found else "Parsed"
                    )
                )
            if csv_found:
                candidate.provenance.append(
                    Provenance(
                        field = "email",
                        value = email,
                        source = "Recruiter CSV",
                        method = "Matched" if resume_found else "Parsed"
                    )
                )

    def _track_phones(self, candidate, resume_candidate, csv_candidate):
        for phone in candidate.phones:
            resume_found = phone in (resume_candidate.phones or [])
            csv_found = phone in (csv_candidate.phones or [])
            if resume_found:
                candidate.provenance.append(
                    Provenance(
                        field = "phone",
                        value = phone,
                        source = "Resume",
                        method = "Matched" if csv_found else "Parsed"
                    )
                )
            if csv_found:
                candidate.provenance.append(
                    Provenance(
                        field = "phone",
                        value = phone,
                        source = "Recruiter CSV",
                        method = "Matched" if resume_found else "Parsed"
                    )
                )

    def _track_links(self, candidate, resume_candidate, csv_candidate):
        candidate_links = candidate.links
        resume_links = resume_candidate.links
        csv_links = csv_candidate.links
        if not candidate_links:
            return
        if candidate_links.linkedin:
            resume_found = (
                resume_links is not None and
                resume_links.linkedin == candidate_links.linkedin
            )
            csv_found = (
                csv_links is not None and
                csv_links.linkedin == candidate_links.linkedin
            )
            if resume_found:
                candidate.provenance.append(
                    Provenance(
                        field="linkedin",
                        value=candidate_links.linkedin,
                        source="Resume",
                        method="Matched" if csv_found else "Parsed"
                    )
                )
            if csv_found:
                candidate.provenance.append(
                    Provenance(
                        field="linkedin",
                        value=candidate_links.linkedin,
                        source="Recruiter CSV",
                        method="Matched" if resume_found else "Parsed"
                    )
                )
        if candidate_links.github:
            resume_found = (
                resume_links is not None and
                resume_links.github == candidate_links.github
            )
            csv_found = (
                csv_links is not None and
                csv_links.github == candidate_links.github
            )
            if resume_found:
                candidate.provenance.append(
                    Provenance(
                        field="github",
                        value=candidate_links.github,
                        source="Resume",
                        method="Matched" if csv_found else "Parsed"
                    )
                )
            if csv_found:
                candidate.provenance.append(
                    Provenance(
                        field="github",
                        value=candidate_links.github,
                        source="Recruiter CSV",
                        method="Matched" if resume_found else "Parsed"
                    )
                )
        if candidate_links.portfolio:
            resume_found = (
                resume_links is not None and
                resume_links.portfolio == candidate_links.portfolio
            )
            csv_found = (
                csv_links is not None and
                csv_links.portfolio == candidate_links.portfolio
            )
            if resume_found:
                candidate.provenance.append(
                    Provenance(
                        field="portfolio",
                        value=candidate_links.portfolio,
                        source="Resume",
                        method="Matched" if csv_found else "Parsed"
                    )
                )
            if csv_found:
                candidate.provenance.append(
                    Provenance(
                        field="portfolio",
                        value=candidate_links.portfolio,
                        source="Recruiter CSV",
                        method="Matched" if resume_found else "Parsed"
                    )
                )
        resume_other = resume_links.other if resume_links else []
        csv_other = csv_links.other if csv_links else []
        for other_link in (candidate_links.other or []):
            resume_found = other_link in (resume_other or [])
            csv_found = other_link in (csv_other or [])
            if resume_found:
                candidate.provenance.append(
                    Provenance(
                        field="other_link",
                        value=other_link,
                        source="Resume",
                        method="Matched" if csv_found else "Parsed"
                    )
                )
            if csv_found:
                candidate.provenance.append(
                    Provenance(
                        field="other_link",
                        value=other_link,
                        source="Recruiter CSV",
                        method="Matched" if resume_found else "Parsed"
                    )
                )
                
    def _track_experience(self, candidate, resume_candidate, csv_candidate):
        for exp in candidate.experience:
            resume_found = any(
                (r.company or "").lower() == (exp.company or "").lower() and (r.title or "").lower() == (exp.title or "").lower()
                for r in (resume_candidate.experience or [])
            )
            csv_found = any(
                (c.company or "").lower() == (exp.company or "").lower() and (c.title or "").lower() == (exp.title or "").lower()
                for c in (csv_candidate.experience or [])
            )
            if resume_found:
                candidate.provenance.append(
                    Provenance(
                        field = "experience",
                        value = f"{exp.company} - {exp.title}",
                        source = "Resume",
                        method = "Matched"
                        if csv_found else "Parsed"
                    )
                )
            if csv_found:
                candidate.provenance.append(
                    Provenance(
                        field = "experience",
                        value = f"{exp.company} - {exp.title}",
                        source = "Recruiter CSV",
                        method = "Matched"
                        if resume_found else "Parsed"
                    )
                )

    def _track_education(self, candidate, resume_candidate, csv_candidate):
        for edu in candidate.education:
            resume_found = any(
                (r.institution or "").lower() == (edu.institution or "").lower() and
                (r.degree or "").lower() == (edu.degree or "").lower()
                for r in (resume_candidate.education or [])
            )
            csv_found = any(
                (r.institution or "").lower() == (edu.institution or "").lower() and
                (r.degree or "").lower() == (edu.degree or "").lower()
                for r in (csv_candidate.education or [])
            )
            if resume_found:
                candidate.provenance.append(
                    Provenance(
                        field = "education",
                        value = f"{edu.institution} - {edu.degree}",
                        source = "Resume",
                        method = "Matched"
                        if csv_found else "Parsed"
                    )
                )
            if csv_found:
                candidate.provenance.append(
                    Provenance(
                        field = "education",
                        value = f"{edu.institution} - {edu.degree}",
                        source = "Recruiter CSV",
                        method = "Matched"
                        if resume_found else "Parsed"
                    )
                )

    def _track_location(self, candidate, resume_candidate, csv_candidate):
        if not candidate.location:
            return
        resume = resume_candidate.location
        csv = csv_candidate.location
        for field in ["city", "region", "country"]:
            value = getattr(candidate.location, field)
            if not value:
                continue
            resume_found = (
                resume is not None and (getattr(resume, field) or "") == value.lower()
            )
            csv_found = (
                csv is not None and (getattr(csv, field) or "") == value.lower()
            )
            if resume_found:
                candidate.provenance.append(
                    Provenance(
                        field = field,
                        value = getattr(candidate.location, field),
                        source = "Resume",
                        method = "Matched" if csv_found else "Parsed"
                    )
                )
            if csv_found:
                candidate.provenance.append(
                    Provenance(
                        field = field,
                        value = getattr(candidate.location, field),
                        source = "Recruiter CSV",
                        method = "Matched" if resume_found else "Parsed"
                    )
                )