EMAIL_REGEX = r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b"
PHONE_REGEX = r"(?:\+?\d{1,3}[\s.-]?)?(?:\(?\d{1,4}\)?[\s.-]?)?\d{3,4}[\s.-]?\d{4}"
LINKEDIN_REGEX = r"https?://(?:www\.)?linkedin\.com/in/[A-Za-z0-9_-]+/?"
GITHUB_REGEX = r"https?://(?:www\.)?github\.com/[A-Za-z0-9_-]+/?"
URL_REGEX = r"https?://[^\s]+"
SKILLS_SECTION_REGEX = (
    r"(?is)"
    r"(?:technical\s+skills|skills|core\s+skills|technologies|technical\s+proficiencies)"
    r"\s*:?\s*"
    r"(.*?)"
    r"(?=\n[A-Z][A-Za-z ]{2,}:?\n|\Z)"
)
DATE_REGEX = (
    r"(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)"
    r"[a-z]*\s+\d{4}"
    r"|"
    r"\d{4}"
    r"|"
    r"Present"
)