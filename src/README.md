# Source Code

The source folder is split into two groups:

```text
src/
  alignment_system.py       core AlignKG system
  entity_extractor.py       ontology entity extraction
  lexical_matcher.py        lexical, token, and n-gram matching
  structural_matcher.py     structural re-ranking
  evaluate_alignments.py    precision/recall/F-score helpers
  isub.py                   lab ISUB similarity code
  runners/                  files you run from the command line
```

## Which File To Run For Each Objective

Run all commands from the repository root.

### OA.1: Alignment System

Core implementation files:

- `src/alignment_system.py`
- `src/entity_extractor.py`
- `src/lexical_matcher.py`
- `src/structural_matcher.py`
- `src/isub.py`

For a one-off ontology pair, run:

```powershell
python src/alignment_system.py --source path\to\source.owl --target path\to\target.owl --output alignments\example\alignkg-source-target.ttl
```

### OA.2: Part 1 Ontology Alignment

Runner:

```text
src/runners/run_part1_alignment.py
```

Command:

```powershell
python src/runners/run_part1_alignment.py --source data\part1\movies_ontology.ttl --target data\part1\schemaorg_movie_external.ttl --output alignments\part1\alignkg-movies-schemaorg.ttl
```

### OA.3: SPARQL Query And CSV Results

Runner:

```text
src/runners/query_part1_graph.py
```

Command:

```powershell
python src/runners/query_part1_graph.py --graph data\part1\movies_ontology.ttl --graph data\part1\schemaorg_movie_external.ttl --graph alignments\part1\alignkg-movies-schemaorg.ttl --query queries\part1_query.sparql --output results\part1_query_results.csv
```

### OA.4: OAEI Evaluation

Runner:

```text
src/runners/run_oaei_tasks.py
```

Overnight command with a two-hour timeout per task:

```powershell
python src/runners/run_oaei_tasks.py --dataset-root data\oaei\OAEI-INM713-IN3067 --output-dir alignments\oaei --results results\oaei_evaluation_results.csv --timeout-seconds 7200
```

The CSV produced by this command is used for the OA.4 results table in `docs/oa4_results.md`.
