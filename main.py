import os
import sys
import json
import argparse

from parsers.resume_parser import ResumeParser
from parsers.csv_parser import CSVParser
from normalizers.candidate_normalizer import CandidateNormalizer
from merger.candidate_merger import CandidateMerger
from merger.confidence import ConfidenceCalculator
from merger.provenance import ProvenanceTracker
from validator.candidate_validator import CandidateValidator
from projector.config_loader import ConfigLoader
from projector.projector import Projector
from projector.output_validator import OutputValidator

def match_and_merge(csv_cands, resume_cand):
    results = []
    resume_matched = False
    resume_emails = set(resume_cand.emails) if resume_cand else set()
    
    for c in csv_cands:
        sources = [("Recruiter CSV", c)]
        is_match = False
        if resume_cand and not resume_matched:
            # Match by email
            c_emails = set(c.emails)
            if resume_emails.intersection(c_emails):
                is_match = True
            # Match by name
            elif c.full_name and resume_cand.full_name and c.full_name.lower() == resume_cand.full_name.lower():
                is_match = True
                
        if is_match:
            sources.append(("Resume", resume_cand))
            resume_matched = True
            
        results.append(sources)
        
    if resume_cand and not resume_matched:
        results.append([("Resume", resume_cand)])
        
    return results

def main():
    parser = argparse.ArgumentParser(description="Multi-Source Candidate Data Transformer")
    parser.add_argument("--csv", help="Path to recruiter CSV")
    parser.add_argument("--resume", help="Path to resume PDF")
    parser.add_argument("--config", default="configs/default.json", help="Output config JSON")
    parser.add_argument("--output", help="Output JSON file path")
    
    args = parser.parse_args()
    
    if not args.csv and not args.resume:
        print("Error: Provide at least one source (--csv or --resume)")
        sys.exit(1)
        
    # Load config
    try:
        config_loader = ConfigLoader()
        config = config_loader.load(args.config)
    except Exception as e:
        print(f"Config error: {e}")
        sys.exit(1)
        
    # Parse sources
    csv_candidates = []
    if args.csv:
        try:
            csv_parser = CSVParser(args.csv)
            csv_candidates = csv_parser.parse()
        except Exception as e:
            print(f"[WARN] CSV parsing failed: {e}. Skipping CSV source.")
            
    resume_candidate = None
    if args.resume:
        try:
            resume_parser = ResumeParser(args.resume)
            resume_candidate = resume_parser.parse()
        except Exception as e:
            print(f"[WARN] Resume parsing failed: {e}. Skipping resume source.")
            
    if not csv_candidates and not resume_candidate:
        print("Error: No valid data extracted from any source.")
        sys.exit(1)
        
    normalizer = CandidateNormalizer()
    
    if resume_candidate:
        resume_candidate = normalizer.normalize(resume_candidate)
        
    normalized_csv = []
    for c in csv_candidates:
        normalized_csv.append(normalizer.normalize(c))
        
    candidate_source_groups = match_and_merge(normalized_csv, resume_candidate)
    
    confidence_calc = ConfidenceCalculator()
    provenance_tracker = ProvenanceTracker()
    canonical_validator = CandidateValidator()
    
    projector = Projector(config)
    output_validator = OutputValidator()
    
    final_outputs = []
    
    for sources in candidate_source_groups:
        merger = CandidateMerger(sources)
        merged_candidate = merger.merge()
        
        if not merged_candidate.candidate_id:
            import hashlib
            id_source = (merged_candidate.emails[0] if merged_candidate.emails else merged_candidate.full_name or "unknown")
            merged_candidate.candidate_id = "gen-" + hashlib.md5(id_source.encode()).hexdigest()[:8]
        
        merged_candidate = confidence_calc.calculate(merged_candidate)
        merged_candidate = provenance_tracker.track(merged_candidate, sources)
        
        try:
            canonical_validator.validate(merged_candidate)
        except Exception as e:
            print(f"[WARN] Canonical validation failed for {merged_candidate.full_name}: {e}")
            
        try:
            projected = projector.project(merged_candidate)
            output_validator.validate(projected, config)
            final_outputs.append(projected)
        except Exception as e:
            print(f"[WARN] Output generation failed for {merged_candidate.full_name}: {e}")
            
    out_json = json.dumps(final_outputs, indent=4)
    if args.output:
        os.makedirs(os.path.dirname(os.path.abspath(args.output)), exist_ok=True)
        with open(args.output, "w", encoding="utf-8") as f:
            f.write(out_json)
        print(f"Processed {len(final_outputs)} candidates. Output saved to {args.output}")
    else:
        print(out_json)

if __name__ == "__main__":
    main()