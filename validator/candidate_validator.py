class CandidateValidator:

    def validate(self, candidate):
        self._validate_required_fields(candidate)
        self._validate_confidence(candidate)
        self._validate_skills(candidate)
        self._validate_emails(candidate)
        self._validate_phones(candidate)
        self._validate_links(candidate)
        self._validate_experience(candidate)
        self._validate_education(candidate)
        self._validate_provenance(candidate)
        return True
    
    def _validate_required_fields(self, candidate):
        if not candidate.full_name or not candidate.full_name.strip():
            raise ValueError("Candidate full name cannot be empty")
        has_email = bool(candidate.emails)
        has_phone = bool(candidate.phones)
        if not has_email and not has_phone:
            raise ValueError(
                "Candidate must have atleast one email or phone number"
            )
        if (candidate.years_experience is not None and
            candidate.years_experience<0):
            raise ValueError("Years of experience cannot be negative")
        return True
    
    def _validate_confidence(self, candidate):
        if not (0<=candidate.overall_confidence<=1):
            raise ValueError(
                "Overall confidence must be between 0 and 1"
            )
        return True
    
    def _validate_skills(self, candidate):
        seen = set()
        for skill in candidate.skills:
            if not skill.name or not skill.name.strip():
                raise ValueError("Skill name cannot be empty")
            key = skill.name.lower()
            if key in seen:
                raise ValueError(
                    f"Duplicate skill found: {skill.name}"
                )
            seen.add(key)
            if not (0<=skill.confidence<=1):
                raise ValueError(
                    f"Invalid confidence for skill: {skill.name}"
                )
        return True
    
    def _validate_emails(self, candidate):
        seen = set()
        for email in candidate.emails:
            if not email or not email.strip():
                raise ValueError("Email cannot be empty")
            key = email.lower()
            if key in seen:
                raise ValueError(
                    f"Duplicate email found: {email}"
                )
            seen.add(key)
        return True
    
    def _validate_phones(self, candidate):
        seen = set()
        for phone in candidate.phones:
            if not phone or not phone.strip():
                raise ValueError("Phone number cannot be empty")
            if phone in seen:
                raise ValueError(
                    f"Duplicate phone number found: {phone}"
                )
            seen.add(phone)
        return True
    
    def _validate_links(self, candidate):
        links = candidate.links
        if not links:
            return True
        if links.linkedin and not links.linkedin.strip():
            raise ValueError("LinkedIn URL cannot be empty")
        if links.github and not links.github.strip():
            raise ValueError("Github URL cannot be empty")
        if links.portfolio and not links.portfolio.strip():
            raise ValueError("Portfolio URL cannot be empty")
        for link in (links.other or []):
            if not link or not link.strip():
                raise ValueError("Other link cannot be empty")
        return True
    
    def _validate_experience(self, candidate):
        for experience in candidate.experience:
            has_company = (
                experience.company and
                experience.company.strip()
            )
            has_title = (
                experience.title and
                experience.title.strip()
            )
            if not has_company and not has_title:
                raise ValueError("Experience must contain atleast a company or title")
        return True
    
    def _validate_education(self, candidate):
        for education in candidate.education:
            has_institution = (
                education.institution and
                education.institution.strip()
            )
            has_degree = (
                education.degree and
                education.degree.strip()
            )
            if not has_institution and not has_degree:
                raise ValueError(
                    "Education must contain atleast an institution or degree"
                )
        return True
    
    def _validate_provenance(self, candidate):
        valid_methods = {"Matched", "Parsed", "Extracted", "Inferred"}
        for provenance in candidate.provenance:
            if not provenance.field or not provenance.field.strip():
                raise ValueError("Provenance field cannot be empty")
            if not provenance.value or not str(provenance.value).strip():
                raise ValueError("Provenance value cannot be empty")
            if not provenance.source or not provenance.source.strip():
                raise ValueError("Provenance source cannot be empty")
            if provenance.method not in valid_methods:
                raise ValueError(
                    f"Invalid provenance method: {provenance.method}"
                )
        return True