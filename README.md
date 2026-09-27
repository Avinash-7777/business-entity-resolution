# Business Entity Resolution

A machine learning / rule-based pipeline for resolving noisy business records across multiple data sources.

## Approach

The project uses:

- Text normalization
- Country-aware blocking
- Business-name matching
- Candidate generation
- Matching result generation

## Project Structure

- ackend/preprocessing.py - text preprocessing and normalization
- ackend/generate_candidates.py - candidate generation
- ackend/make_final.py - final matching result generation
- ackend/ - supporting experiments and evaluation scripts

## Dataset

The competition dataset is not included in this repository.

## Output

The competition generates:

- matching_results.tsv
- candidate_pairs.tsv

Generated datasets and submission files are excluded from Git using .gitignore.

## Competition

Business Entity Resolution Hackathon.

