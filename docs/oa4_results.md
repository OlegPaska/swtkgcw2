# OA.4 Evaluation Results

AlignKG was evaluated with the official coursework OAEI dataset package under:

```text
data/oaei/OAEI-INM713-IN3067/
```

The generated alignments are stored in `alignments/oaei/`.

The evaluation CSV is stored in `results/oaei_evaluation_results.csv`.

## Summary

| Track | Tasks | Completed | Timed out | Other status | Average F-score completed |
| --- | ---: | ---: | ---: | ---: | ---: |
| anatomy | 1 | 1 | 0 | 0 | 0.676 |
| bio-ml | 5 | 3 | 2 | 0 | 0.347 |
| circular-economy | 2 | 2 | 0 | 0 | 0.363 |
| conference | 21 | 21 | 0 | 0 | 0.453 |
| digital-humanities | 8 | 8 | 0 | 0 | 0.000 |
| knowledge-graph | 5 | 0 | 5 | 0 | - |

Overall:

- Total tasks reported: 42
- Completed tasks: 35
- Timed-out tasks: 7

## Per-Task Results

| Task | Track | Status | Precision | Recall | F-score | Runtime seconds | Mappings |
| --- | --- | --- | ---: | ---: | ---: | ---: | ---: |
| human-mouse | anatomy | ok | 0.582 | 0.806 | 0.676 | 103.865 | 2099 |
| ncit-doid | bio-ml | ok | 0.348 | 0.669 | 0.458 | 1659.793 | 8991 |
| omim-ordo | bio-ml | ok | 0.313 | 0.461 | 0.373 | 3183.345 | 5480 |
| snomed.body-fma.body | bio-ml | timeout_after_7200_seconds | 0.000 | 0.000 | 0.000 | 7200.000 | 0 |
| snomed.neoplas-ncit.neoplas | bio-ml | ok | 0.164 | 0.292 | 0.210 | 6340.696 | 6799 |
| snomed.pharm-ncit.pharm | bio-ml | timeout_after_7200_seconds | 0.000 | 0.000 | 0.000 | 7200.000 | 0 |
| CEON-BiOnto | circular-economy | ok | 0.290 | 0.931 | 0.443 | 1.752 | 93 |
| CEON-MATONTO | circular-economy | ok | 0.167 | 0.938 | 0.283 | 5.652 | 90 |
| cmt-conference | conference | ok | 0.316 | 0.400 | 0.353 | 0.429 | 19 |
| cmt-confOf | conference | ok | 0.385 | 0.312 | 0.345 | 0.148 | 13 |
| cmt-edas | conference | ok | 0.474 | 0.692 | 0.562 | 0.294 | 19 |
| cmt-ekaw | conference | ok | 0.333 | 0.455 | 0.385 | 0.192 | 15 |
| cmt-iasted | conference | ok | 0.308 | 1.000 | 0.471 | 0.337 | 13 |
| cmt-sigkdd | conference | ok | 0.500 | 0.750 | 0.600 | 0.162 | 18 |
| conference-confOf | conference | ok | 0.306 | 0.733 | 0.431 | 0.286 | 36 |
| conference-edas | conference | ok | 0.278 | 0.588 | 0.377 | 0.500 | 36 |
| conference-ekaw | conference | ok | 0.333 | 0.480 | 0.393 | 0.207 | 36 |
| conference-iasted | conference | ok | 0.190 | 0.286 | 0.229 | 0.387 | 21 |
| conference-sigkdd | conference | ok | 0.360 | 0.600 | 0.450 | 0.190 | 25 |
| confOf-edas | conference | ok | 0.545 | 0.632 | 0.585 | 0.296 | 22 |
| confOf-ekaw | conference | ok | 0.611 | 0.550 | 0.579 | 0.157 | 18 |
| confOf-iasted | conference | ok | 0.400 | 0.444 | 0.421 | 0.230 | 10 |
| confOf-sigkdd | conference | ok | 0.800 | 0.571 | 0.667 | 0.133 | 5 |
| edas-ekaw | conference | ok | 0.379 | 0.478 | 0.423 | 0.310 | 29 |
| edas-iasted | conference | ok | 0.348 | 0.421 | 0.381 | 0.493 | 23 |
| edas-sigkdd | conference | ok | 0.438 | 0.467 | 0.452 | 0.298 | 16 |
| ekaw-iasted | conference | ok | 0.261 | 0.600 | 0.364 | 0.365 | 23 |
| ekaw-sigkdd | conference | ok | 0.438 | 0.636 | 0.519 | 0.185 | 16 |
| iasted-sigkdd | conference | ok | 0.368 | 0.933 | 0.528 | 0.336 | 38 |
| defc-pactols | digital-humanities | ok | 0.000 | 0.000 | 0.000 | 3.779 | 1 |
| dha-unesco | digital-humanities | ok | 0.000 | 0.000 | 0.000 | 2.388 | 1 |
| idai-pactols | digital-humanities | ok | 0.000 | 0.000 | 0.000 | 1.387 | 1 |
| idai-parthenos | digital-humanities | ok | 0.000 | 0.000 | 0.000 | 1.958 | 1 |
| ironagedanube-pactols | digital-humanities | ok | 0.000 | 0.000 | 0.000 | 0.501 | 1 |
| oeai-parthenos | digital-humanities | ok | 0.000 | 0.000 | 0.000 | 3.489 | 1 |
| pactols-parthenos | digital-humanities | ok | 0.000 | 0.000 | 0.000 | 0.258 | 1 |
| tadirah-unesco | digital-humanities | ok | 0.000 | 0.000 | 0.000 | 2.893 | 2 |
| marvelcinematicuniverse-marvel | knowledge-graph | timeout_after_120_seconds | 0.000 | 0.000 | 0.000 | 120.000 | 0 |
| memoryalpha-memorybeta | knowledge-graph | timeout_after_120_seconds | 0.000 | 0.000 | 0.000 | 120.000 | 0 |
| memoryalpha-stexpanded | knowledge-graph | timeout_after_120_seconds | 0.000 | 0.000 | 0.000 | 120.000 | 0 |
| starwars-swg | knowledge-graph | timeout_after_120_seconds | 0.000 | 0.000 | 0.000 | 120.000 | 0 |
| starwars-swtor | knowledge-graph | timeout_after_120_seconds | 0.000 | 0.000 | 0.000 | 120.000 | 0 |

## Discussion

The results show that AlignKG is strongest when equivalent entities share labels, URI fragments, or closely related tokens. This is visible in the anatomy, circular economy, and conference tracks.

Lower scores or timeouts indicate the limitations of a lightweight lexical and structural matcher. The digital humanities track is challenging because multilingual and domain-specific vocabularies often do not share obvious lexical forms. The Bio-ML and Knowledge Graph tracks are challenging because of ontology size and therefore test scalability more strongly.

The timeout setting follows the coursework guidance to report tasks that do not finish within a fixed limit.
