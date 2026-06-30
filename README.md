# Eightfold Candidate Data Transformer

A robust, multi-source pipeline that unifies unstructured (Resume) and structured (CSV) candidate data into configurable downstream schemas.

## Overview
This tool ingests unstructured candidate resumes and semi-structured recruiter CSV data, parses them, normalizes the data to a standard format (E.164 phone numbers, ISO-3166 countries, and canonical skill mapping), matches the candidates across sources using heuristic identity resolution (email, name), merges the unified data, and projects the final unified profiles to customizable JSON schemas dynamically.

## Installation

```bash
pip install -r requirements.txt
```

## Usage

```bash
python main.py --csv input/recruiter.csv --resume input/resume.pdf --config configs/custom.json --output output/custom_candidates.json
```

**Arguments:**
- `--csv`: Path to the recruiter CSV
- `--resume`: Path to the resume PDF
- `--config`: Path to the JSON configuration file determining the output projection structure
- `--output`: Output JSON path

You can provide either `--csv` or `--resume` or both. The pipeline gracefully processes whichever source is provided, matching records if both are given.

## Architecture

1. **Parsers**: Independent extractors for unstructured and semi-structured sources.
2. **Normalizers**: Formatting data to E.164 (phones), ISO-3166 (locations), lowercasing emails, and applying alias dictionaries to skills (e.g. `js -> JavaScript`).
3. **Matcher & Merger**: Resolves identities across different sources using emails and names. Merges N sources to produce a unified candidate record, tracking confidence and field provenance.
4. **Projector**: A custom projection layer that translates the internal candidate schema into a target client format driven by declarative JSON configuration.
5. **Validator**: Validates the outgoing data structure against the schema definitions.

## Configuration Engine

You can completely alter the outgoing format by supplying a custom JSON config. The JSON structure uses dot notation and `[]` syntax for deep extraction:

```json
{
  "fields": [
    {
      "path": "full_name",
      "type": "string",
      "required": true
    },
    {
      "path": "primary_email",
      "from": "emails[0]",
      "type": "string",
      "required": true
    }
  ]
}
```

## Tests

To run the unit tests:
```bash
pytest tests/
```