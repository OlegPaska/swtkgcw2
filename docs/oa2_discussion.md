# OA.2 Discussion

OA.2 aligns the Part 1 movie ontology, `data/part1/movies_ontology.ttl`, with the external Schema.org module, `data/part1/schemaorg_movie_external.ttl`. Schema.org was chosen because it has obvious overlap with a movie ontology, including terms for movies, people, actors, directors, genres, names, runtimes, and places. The alignment was generated with `src/runners/run_part1_alignment.py` and saved as `alignments/part1/alignkg-movies-schemaorg.ttl`.

## Generated Mappings

The final alignment contains 11 mappings: 5 `owl:equivalentClass` mappings and 6 `owl:equivalentProperty` mappings. The class mappings are `Movie` to `schema:Movie`, `Person` to `schema:Person`, `City` to `schema:City`, `Country` to `schema:Country`, and `Action` to `schema:Action`. The property mappings are `HasActor` to `schema:actor`, `HasDirector` to `schema:director`, `HasGenre` to `schema:genre`, `FromLocation` to `schema:fromLocation`, `name` to `schema:name`, and `runtime` to `schema:runtime`. No individual mappings were produced.

## Matching Approach

AlignKG extracts classes, properties, and individuals with `rdflib`, then compares only compatible entity types. The matching is mainly lexical, using normalised labels and URI local names with exact matching, ISUB, Jaro-Winkler, token Jaccard, and character n-gram similarity. It also uses a small structural boost from domains, ranges, parent/child classes, and RDF types, which helps with properties such as `HasActor` and `HasDirector`.

## Good Mappings

The strongest mappings are the obvious movie-domain ones: `Movie` to `schema:Movie`, `Person` to `schema:Person`, `HasActor` to `schema:actor`, `HasDirector` to `schema:director`, and `HasGenre` to `schema:genre`. These are good because the labels are very close and the intended meaning is the same. `name` to `schema:name` and `runtime` to `schema:runtime` are also reasonable literal-property mappings.

## Weaker Or Missing Mappings

Some local modelling classes were left unmapped because Schema.org does not have direct equivalents for every coursework-specific class. This is acceptable because forcing weak mappings would reduce precision. The weakest included mapping is probably `Action` to `schema:Action`, because the local ontology may use Action as a film genre, while Schema.org uses `Action` more broadly.

## Limitations

The alignment is deliberately simple. AlignKG does not use embeddings, a reasoner, or external background knowledge, so it works best when equivalent terms have similar names. Schema.org is also much larger and broader than the local movie ontology, so high thresholds were used to keep the output conservative. For OA.2 this is enough: it links the Part 1 ontology to an external ontology and provides mappings that can be queried in OA.3.
