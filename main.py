from parsers.csv_parser import CSVParser

parser = CSVParser("input/recruiter.csv")
candidates = parser.parse()
for candidate in candidates:
    print(candidate.model_dump())