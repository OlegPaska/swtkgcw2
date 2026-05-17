import argparse
import os
import time

from rdflib import Graph, URIRef
from rdflib.namespace import OWL, RDF, RDFS

from entity_extractor import EntityExtractor
from lexical_matcher import LexicalMatcher
from structural_matcher import StructuralMatcher


class AlignKG(object):
    def __init__(
        self,
        class_threshold=0.86,
        property_threshold=0.84,
        individual_threshold=0.92,
        candidate_limit=200,
    ):
        self.class_threshold = class_threshold
        self.property_threshold = property_threshold
        self.individual_threshold = individual_threshold
        self.candidate_limit = candidate_limit
        self.lexical_matcher = LexicalMatcher(candidate_limit=candidate_limit)
        self.structural_matcher = StructuralMatcher()
        self.mappings = []
        self.runtime_seconds = 0.0

    def matchOntologies(self, source_file, target_file):
        start = time.perf_counter()

        source = EntityExtractor(source_file).extractAll()
        target = EntityExtractor(target_file).extractAll()

        class_mappings = self.lexical_matcher.matchEntities(
            source["classes"],
            target["classes"],
            "class",
            self.class_threshold,
        )
        property_mappings = self.lexical_matcher.matchEntities(
            source["properties"],
            target["properties"],
            "property",
            self.property_threshold,
        )
        individual_mappings = self.lexical_matcher.matchEntities(
            source["individuals"],
            target["individuals"],
            "individual",
            self.individual_threshold,
        )

        self.mappings = self.structural_matcher.rerankMappings(
            class_mappings + property_mappings + individual_mappings
        )
        self.runtime_seconds = time.perf_counter() - start
        return self.mappings

    def mappingPredicate(self, mapping):
        if mapping.entity_type == "class":
            return OWL.equivalentClass
        if mapping.entity_type == "property":
            return OWL.equivalentProperty
        return OWL.sameAs

    def createAlignmentGraph(self):
        g = Graph()
        g.bind("owl", OWL)
        g.bind("rdf", RDF)
        g.bind("rdfs", RDFS)

        for mapping in self.mappings:
            g.add((
                URIRef(mapping.source.iri),
                self.mappingPredicate(mapping),
                URIRef(mapping.target.iri),
            ))

        return g

    def saveAlignment(self, output_file):
        output_dir = os.path.dirname(output_file)
        if output_dir:
            os.makedirs(output_dir, exist_ok=True)
        self.createAlignmentGraph().serialize(destination=output_file, format="ttl")

    def run(self, source_file, target_file, output_file):
        self.matchOntologies(source_file, target_file)
        self.saveAlignment(output_file)
        print("Mappings: " + str(len(self.mappings)))
        print("Runtime seconds: " + str(round(self.runtime_seconds, 3)))
        print("Saved alignment: " + output_file)


def main():
    parser = argparse.ArgumentParser(description="Run AlignKG on two ontology files.")
    parser.add_argument("--source", required=True)
    parser.add_argument("--target", required=True)
    parser.add_argument("--output", required=True)
    parser.add_argument("--class-threshold", type=float, default=0.86)
    parser.add_argument("--property-threshold", type=float, default=0.84)
    parser.add_argument("--individual-threshold", type=float, default=0.92)
    parser.add_argument("--candidate-limit", type=int, default=200)
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

