from parsers.resume_parser import ResumeParser
# from parsers.csv_parser import CSVParser

parser = ResumeParser("input/resume.pdf")
candidate = parser.parse()
print(candidate.model_dump())