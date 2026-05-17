import argparse
import csv
import os
import multiprocessing
import queue as queue_module
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[1]))

from alignment_system import AlignKG
from evaluate_alignments import compareWithReference, saveEvaluationRows


def findOntologyFile(ontologies_dir, ontology_name):
    for extension in [".owl", ".rdf", ".ttl", ".xml"]:
        candidate = ontologies_dir / (ontology_name + extension)
        if candidate.exists():
            return candidate
    return None


def iterReferenceAlignments(dataset_root):
    root = Path(dataset_root)
    for reference_file in root.rglob("*.ttl"):
        if "ontologies" in [part.lower() for part in reference_file.parts]:
            continue
        if "alignments" in [part.lower() for part in reference_file.parts]:
            continue
        if "reference" in str(reference_file.parent).lower() or reference_file.parent.name != "ontologies":
            yield reference_file


def emptyMetrics(row, status, system_output=""):
    row.update({
        "system": str(system_output),
        "true_positives": 0,
        "false_positives": 0,
        "false_negatives": 0,
        "precision": 0.0,
        "recall": 0.0,
        "f_score": 0.0,
        "system_mappings": 0,
        "reference_mappings": 0,
        "status": status,
    })
    return row


def runMatcherProcess(source_file, target_file, system_output, queue):
    try:
        matcher = AlignKG()
        matcher.run(str(source_file), str(target_file), str(system_output))
        queue.put({
            "status": "ok",
            "runtime_seconds": round(matcher.runtime_seconds, 3),
        })
    except Exception as err:
        queue.put({
            "status": "error: " + str(err),
            "runtime_seconds": "",
        })


def runTaskWithTimeout(source_file, target_file, system_output, timeout_seconds):
    result_queue = multiprocessing.Queue()
    process = multiprocessing.Process(
        target=runMatcherProcess,
        args=(source_file, target_file, system_output, result_queue),
    )
    process.start()
    process.join(timeout_seconds)

    if process.is_alive():
        process.terminate()
        process.join()
        return {
            "status": "timeout_after_" + str(timeout_seconds) + "_seconds",
            "runtime_seconds": timeout_seconds,
        }

    try:
        return result_queue.get(timeout=5)
    except queue_module.Empty:
        pass

    return {
        "status": "error: matcher process finished without returning a result",
        "runtime_seconds": "",
    }


def runTasks(dataset_root, output_dir, results_file, timeout_seconds=7200):
    rows = []
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)

    for reference_file in iterReferenceAlignments(dataset_root):
        task_name = reference_file.stem
        parts = task_name.split("-")
        if len(parts) < 2:
            continue

        source_name = parts[0]
        target_name = "-".join(parts[1:])
        task_root = reference_file.parent.parent
        if reference_file.parent.name != "reference-alignments":
            task_root = reference_file.parent
        ontologies_dir = task_root / "ontologies"

        source_file = findOntologyFile(ontologies_dir, source_name)
        target_file = findOntologyFile(ontologies_dir, target_name)
        system_output = output_path / reference_file.parent.name / ("alignkg-" + task_name + ".ttl")
        system_output.parent.mkdir(parents=True, exist_ok=True)

        row = {
            "task": task_name,
            "reference": str(reference_file),
            "runtime_seconds": "",
            "status": "not_started",
        }

        if source_file is None or target_file is None:
            rows.append(emptyMetrics(row, "missing_ontology_file", system_output))
            continue

        try:
            run_result = runTaskWithTimeout(source_file, target_file, system_output, timeout_seconds)

            if run_result["status"] != "ok":
                row["runtime_seconds"] = run_result["runtime_seconds"]
                rows.append(emptyMetrics(row, run_result["status"], system_output))
            else:
                metrics = compareWithReference(str(reference_file), str(system_output))
                metrics["task"] = task_name
                metrics["runtime_seconds"] = run_result["runtime_seconds"]
                metrics["status"] = "ok"
                rows.append(metrics)
        except Exception as err:
            row.update({
                "system": str(system_output),
                "true_positives": 0,
                "false_positives": 0,
                "false_negatives": 0,
                "precision": 0.0,
                "recall": 0.0,
                "f_score": 0.0,
                "system_mappings": 0,
                "reference_mappings": 0,
                "status": "error: " + str(err),
            })
            rows.append(row)

    saveEvaluationRows(rows, results_file)
    print("Saved OAEI evaluation results: " + results_file)


def rerunFailedTasks(results_file, timeout_seconds=120, retry_status="error: matcher process finished without returning a result"):
    with open(results_file, newline="", encoding="utf-8") as csv_file:
        rows = list(csv.DictReader(csv_file))

    retried = 0
    improved = 0

    for row in rows:
        if row.get("status") != retry_status:
            continue

        retried += 1
        task_name = row["task"]
        parts = task_name.split("-")
        if len(parts) < 2:
            emptyMetrics(row, "error: cannot derive ontology names from task name", row.get("system", ""))
            continue

        reference_file = Path(row["reference"])
        task_root = reference_file.parent.parent
        if reference_file.parent.name != "reference-alignments":
            task_root = reference_file.parent
        ontologies_dir = task_root / "ontologies"

        source_file = findOntologyFile(ontologies_dir, parts[0])
        target_file = findOntologyFile(ontologies_dir, "-".join(parts[1:]))
        system_output = Path(row["system"])
        system_output.parent.mkdir(parents=True, exist_ok=True)

        print("Retrying " + task_name + " with " + str(timeout_seconds) + "s timeout...")

        if source_file is None or target_file is None:
            row["runtime_seconds"] = ""
            emptyMetrics(row, "error: missing ontology file", system_output)
            continue

        run_result = runTaskWithTimeout(source_file, target_file, system_output, timeout_seconds)
        row["runtime_seconds"] = run_result.get("runtime_seconds", "")

        if run_result["status"] == "ok":
            metrics = compareWithReference(str(reference_file), str(system_output))
            row.update(metrics)
            row["task"] = task_name
            row["runtime_seconds"] = run_result["runtime_seconds"]
            row["status"] = "ok"
            improved += 1
        else:
            emptyMetrics(row, run_result["status"], system_output)
            row["runtime_seconds"] = run_result.get("runtime_seconds", "")

    saveEvaluationRows(rows, results_file)
    print("Retried failed OAEI tasks: " + str(retried))
    print("Rows changed to ok: " + str(improved))
    print("Saved OAEI evaluation results: " + results_file)


def main():
    parser = argparse.ArgumentParser(description="Run AlignKG over OAEI-style coursework tasks.")
    parser.add_argument("--dataset-root", default="data/oaei")
    parser.add_argument("--output-dir", default="alignments/oaei")
    parser.add_argument("--results", default="results/oaei_evaluation_results.csv")
    parser.add_argument("--timeout-seconds", type=int, default=7200)
    parser.add_argument("--retry-failed-only", action="store_true")
    args = parser.parse_args()

    if args.retry_failed_only:
        rerunFailedTasks(args.results, timeout_seconds=args.timeout_seconds)
    else:
        runTasks(args.dataset_root, args.output_dir, args.results, timeout_seconds=args.timeout_seconds)


if __name__ == "__main__":
    main()
