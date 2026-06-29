from parsers.resume_parser import ResumeParser

parser = ResumeParser("input/resume.pdf")
candidate = parser.parse()
print(candidate.model_dump())