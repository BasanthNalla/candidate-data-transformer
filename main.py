from parsers.resume_parser import ResumeParser
from parsers.csv_parser import CSVParser

from normalizers.candidate_normalizer import CandidateNormalizer
from merger.candidate_merger import CandidateMerger

csv_parser = CSVParser("input/recruiter.csv")
resume_parser = ResumeParser("input/resume.pdf")

csv_candidates = csv_parser.parse()
resume_candidate = resume_parser.parse()

normalizer = CandidateNormalizer()

resume_candidate = normalizer.normalize(resume_candidate)
csv_candidates = [
    normalizer.normalize(candidate)
    for candidate in csv_candidates
]

merger = CandidateMerger(
    resume_candidate,
    csv_candidates[0]
)

merged_candidate = merger.merge()
print(merged_candidate.model_dump())