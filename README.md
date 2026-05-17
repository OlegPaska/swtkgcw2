# AlignKG

Coursework solution for IN3067/INM713 Coursework Part 2: Ontology Alignment.

AlignKG is a Python ontology alignment system inspired by the `python-2026` lab examples. It uses `rdflib.Graph` for RDF handling, the lab `isub.py` lexical similarity code, Turtle output, and simple command-line runners.

## Contents

```text
alignments/             generated Turtle alignment files
data/                   Part 1 ontologies and OAEI coursework dataset
docs/                   system description, OA.2 discussion, and OA.4 results
queries/                SPARQL query for OA.3
results/                CSV outputs
src/                    AlignKG implementation and command-line runners
submission-package/     generated source-code PDF, source text, zip, and repository link file
```

The most useful code guide is `src/README.md`, which states exactly which runner file to use for each coursework objective.

## Data And Outputs

Part 1 uses:

```text
data/part1/movies_ontology.ttl
data/part1/schemaorg_movie_external.ttl
```

`movies_ontology.ttl` is the main local movie ontology. `schemaorg_movie_external.ttl` is a filtered Schema.org module derived from the downloaded Schema.org Turtle vocabulary.

OA.2 output:

```text
alignments/part1/alignkg-movies-schemaorg.ttl
```

OA.3 output:

```text
results/part1_query_results.csv
```

OA.4 uses the official coursework OAEI dataset package:

```text
data/oaei/OAEI-INM713-IN3067/
```

This contains the anatomy, bio-ml, circular-economy, conference, digital-humanities, and knowledge-graph tracks. OA.4 outputs are stored in:

```text
alignments/oaei/
results/oaei_evaluation_results.csv
docs/oa4_results.md
```

## Results Summary

Detailed OA.4 results are in `docs/oa4_results.md` and `results/oaei_evaluation_results.csv`.

| Track | Tasks | Completed | Timed out | Other status |
| --- | ---: | ---: | ---: | ---: |
| Anatomy | 1 | 1 | 0 | 0 |
| Bio-ML | 5 | 3 | 2 | 0 |
| Circular Economy | 2 | 2 | 0 | 0 |
| Conference | 21 | 21 | 0 | 0 |
| Digital Humanities | 8 | 8 | 0 | 0 |
| Knowledge Graph | 5 | 0 | 5 | 0 |

Overall, 35 of 42 OAEI tasks completed and 7 timed out.

## Install

Run from this folder:

```powershell
python -m pip install -r requirements.txt
```

## Main Commands

Run all commands from the repository root.

OA.1/OA.2 one-off alignment:

```powershell
python src/runners/run_part1_alignment.py --source data\part1\movies_ontology.ttl --target data\part1\schemaorg_movie_external.ttl --output alignments\part1\alignkg-movies-schemaorg.ttl
```

OA.3 SPARQL query:

```powershell
python src/runners/query_part1_graph.py --graph data\part1\movies_ontology.ttl --graph data\part1\schemaorg_movie_external.ttl --graph alignments\part1\alignkg-movies-schemaorg.ttl --query queries\part1_query.sparql --output results\part1_query_results.csv
```

OA.4 full OAEI run with a two-hour timeout per task:

```powershell
python src/runners/run_oaei_tasks.py --dataset-root data\oaei\OAEI-INM713-IN3067 --output-dir alignments\oaei --results results\oaei_evaluation_results.csv --timeout-seconds 7200
```

The OAEI runner records long-running tasks as timeout rows in the CSV.
