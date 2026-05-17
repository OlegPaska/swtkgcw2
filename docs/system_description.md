# System Description

System name: AlignKG.

AlignKG is an ontology alignment system implemented in Python. It follows the style of the module lab examples: small scripts, `rdflib.Graph` for RDF handling, Turtle serialisation, and the lab ISUB implementation for lexical similarity.

Implemented techniques:

- lexical matching over `rdfs:label` values and URI local names
- exact normalised label matching
- ISUB similarity
- Jaro-Winkler similarity via `python-Levenshtein`
- token Jaccard similarity
- character n-gram vector cosine similarity
- entity-type aware matching for classes, properties, and individuals
- token blocking to reduce the number of pairwise comparisons
- candidate limits for larger ontologies
- structural/contextual score boosts from parents, children, domains, ranges, and RDF types
- filtering of annotation properties and weak no-token-overlap candidates to reduce false positives

Output predicates:

- class mappings use `owl:equivalentClass`
- property mappings use `owl:equivalentProperty`
- individual mappings use `owl:sameAs`

This implementation is limited to lexical and structural matching. Embeddings and LLM-based matching were not used.

The external OA.2 ontology currently used is a Schema.org Turtle module saved at `data/part1/schemaorg_movie_external.ttl`.
