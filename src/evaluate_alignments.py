import argparse
import csv
import os

from rdflib import Graph
from rdflib.util import guess_format


def loadMappings(mapping_file):
    g = Graph()
    g.parse(mapping_file, format=guess_format(mapping_file))
    return g


def compareWithReference(reference_mappings_file, system_mappings_file):
    ref_mappings = loadMappings(reference_mappings_file)
    system_mappings = loadMappings(system_mappings_file)

    tp = 0
    fp = 0
    fn = 0

    for s, p, o in system_mappings:
        if (s, p, o) in ref_mappings or (o, p, s) in ref_mappings:
            tp += 1
        else:
            fp += 1

    for s, p, o in ref_mappings:
        if (s, p, o) not in system_mappings and (o, p, s) not in system_mappings:
            fn += 1

    precision = tp / (tp + fp) if (tp + fp) > 0 else 0.0
    recall = tp / (tp + fn) if (tp + fn) > 0 else 0.0
    f_score = (2 * precision * recall) / (precision + recall) if (precision + recall) > 0 else 0.0

    return {
        "reference": reference_mappings_file,
        "system": system_mappings_file,
        "true_positives": tp,
        "false_positives": fp,
        "false_negatives": fn,
        "precision": precision,
        "recall": recall,
        "f_score": f_score,
        "system_mappings": len(system_mappings),
        "reference_mappings": len(ref_mappings),
    }


def saveEvaluationRows(rows, output_file):
    output_dir = os.path.dirname(output_file)
    if output_dir:
        os.makedirs(output_dir, exist_ok=True)

    fieldnames = [
        "task",
        "reference",
        "system",
        "true_positives",
        "false_positives",
        "false_negatives",
        "precision",
        "recall",
        "f_score",
        "runtime_seconds",
        "system_mappings",
        "reference_mappings",
        "status",
    ]

    with open(output_file, "w", newline="", encoding="utf-8") as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            writer.writerow(row)


def main():
    parser = argparse.ArgumentParser(description="Evaluate one alignment against a reference alignment.")
    parser.add_argument("--reference", required=True)
    parser.add_argument("--system", required=True)
    args = parser.parse_args()

    results = compareWithReference(args.reference, args.system)
    print("Precision: " + str(results["precision"]))
    print("Recall: " + str(results["recall"]))
    print("F-Score: " + str(results["f_score"]))


if __name__ == "__main__":
    main()

