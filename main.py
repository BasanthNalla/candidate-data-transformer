import os

from parsers.resume_parser import ResumeParser
from parsers.csv_parser import CSVParser

from normalizers.candidate_normalizer import CandidateNormalizer

from merger.candidate_merger import CandidateMerger
from merger.confidence import ConfidenceCalculator
from merger.provenance import ProvenanceTracker

from validator.candidate_validator import CandidateValidator

def main():

    csv_parser = CSVParser("input/recruiter.csv")
    resume_parser = ResumeParser("input/resume.pdf")

    csv_candidates = csv_parser.parse()
    resume_candidate = resume_parser.parse()

    if not csv_candidates:
        raise ValueError("No candidates found in recruiter CSV")

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

    confidence = ConfidenceCalculator()
    merged_candidate = confidence.calculate(merged_candidate)

    tracker = ProvenanceTracker()

    merged_candidate = tracker.track(
        merged_candidate, resume_candidate, csv_candidates[0]
    )

    validator = CandidateValidator()

    validator.validate(merged_candidate)

    os.makedirs("output", exist_ok=True)
    output_file = "output/candidate.json"
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(merged_candidate.model_dump_json(indent=4))

    print("Candidate transformation completed successfully.")
    print(f"Output saved to: {output_file}")

if __name__ == "__main__":
    main()