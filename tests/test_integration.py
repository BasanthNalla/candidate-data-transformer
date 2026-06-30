import os
from parsers.csv_parser import CSVParser
from merger.candidate_merger import CandidateMerger
from merger.confidence import ConfidenceCalculator
from merger.provenance import ProvenanceTracker

def test_john_smith_gold_profile():
    input_dir = os.path.join(os.path.dirname(__file__), "..", "input")
    csv_path = os.path.join(input_dir, "recruiter.csv")
    
    parser = CSVParser(csv_path)
    candidates = parser.parse()
    
    johns = [c for c in candidates if c.full_name == "John Smith"]
    assert len(johns) == 1
    john = johns[0]
    
    from normalizers.candidate_normalizer import CandidateNormalizer
    
    merger = CandidateMerger([("Recruiter CSV", john)])
    merged = merger.merge()
    merged = CandidateNormalizer().normalize(merged)
    
    calc = ConfidenceCalculator()
    merged = calc.calculate(merged)
    tracker = ProvenanceTracker()
    merged = tracker.track(merged, [("Recruiter CSV", john)])
    
    assert merged.full_name == "John Smith"
    assert merged.emails == ["john.smith@gmail.com"]
    assert merged.phones == ["+919876543210"]
    assert merged.location.city == "Hyderabad"
    assert merged.location.country == "IN"
    assert merged.years_experience == 3.0
    assert len(merged.skills) == 4
