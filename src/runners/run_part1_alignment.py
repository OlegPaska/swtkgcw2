import argparse
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[1]))

from alignment_system import AlignKG


def main():
    parser = argparse.ArgumentParser(description="Run AlignKG for OA.2 Part 1 ontology alignment.")
    parser.add_argument("--source", default="data/part1/movies_ontology.ttl")
    parser.add_argument("--target", required=True)
    parser.add_argument("--output", default="alignments/part1/alignkg-part1.ttl")
    parser.add_argument("--class-threshold", type=float, default=0.90)
    parser.add_argument("--property-threshold", type=float, default=0.92)
    parser.add_argument("--individual-threshold", type=float, default=0.92)
    parser.add_argument("--candidate-limit", type=int, default=500)
    args = parser.parse_args()

    system = AlignKG(
        class_threshold=args.class_threshold,
        property_threshold=args.property_threshold,
        individual_threshold=args.individual_threshold,
        candidate_limit=args.candidate_limit,
    )
    system.run(args.source, args.target, args.output)


if __name__ == "__main__":
    main()

