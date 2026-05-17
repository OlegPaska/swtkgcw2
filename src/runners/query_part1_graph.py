import argparse
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[1]))
import csv
import os

from rdflib import Graph
from rdflib.util import guess_format
import owlrl


def loadGraph(files):
    g = Graph()
    for file_path in files:
        g.parse(file_path, format=guess_format(file_path))
    return g


def runQuery(graph_files, query_file, output_file, use_reasoning=True):
    g = loadGraph(graph_files)

    print("Loaded '" + str(len(g)) + "' triples.")

    if use_reasoning:
        owlrl.DeductiveClosure(
            owlrl.OWLRL_Semantics,
            axiomatic_triples=False,
            datatype_axioms=False,
        ).expand(g)
        print("Triples after OWL 2 RL reasoning: '" + str(len(g)) + "'.")

    query = open(query_file, "r", encoding="utf-8-sig").read()
    qres = g.query(query)

    output_dir = os.path.dirname(output_file)
    if output_dir:
        os.makedirs(output_dir, exist_ok=True)

    with open(output_file, "w", newline="", encoding="utf-8") as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow([str(var) for var in qres.vars])
        for row in qres:
            writer.writerow([str(value) for value in row])

    print("Saved query results: " + output_file)


def main():
    parser = argparse.ArgumentParser(description="Run the OA.3 SPARQL query over aligned Part 1 graphs.")
    parser.add_argument("--graph", action="append", required=True, help="Ontology, data, or alignment file to load.")
    parser.add_argument("--query", default="queries/part1_query.sparql")
    parser.add_argument("--output", default="results/part1_query_results.csv")
    parser.add_argument("--no-reasoning", action="store_true")
    args = parser.parse_args()

    runQuery(args.graph, args.query, args.output, use_reasoning=not args.no_reasoning)


if __name__ == "__main__":
    main()

