from dataclasses import dataclass
from collections import defaultdict

try:
    import Levenshtein as lev
except ImportError:
    lev = None

from isub import isub


@dataclass
class CandidateMapping:
    source: object
    target: object
    entity_type: str
    lexical_score: float
    structural_score: float = 0.0
    final_score: float = 0.0


def jaccard(tokens1, tokens2):
    if not tokens1 or not tokens2:
        return 0.0
    intersection = len(tokens1.intersection(tokens2))
    union = len(tokens1.union(tokens2))
    return intersection / union


def characterNgrams(label, n=3):
    label = " " + label + " "
    if len(label) < n:
        return {label}
    return {label[index:index + n] for index in range(len(label) - n + 1)}


def cosineFromSets(values1, values2):
    if not values1 or not values2:
        return 0.0
    intersection = len(values1.intersection(values2))
    return intersection / ((len(values1) * len(values2)) ** 0.5)


class LexicalMatcher(object):
    def __init__(self, threshold=0.86, candidate_limit=200):
        self.threshold = threshold
        self.candidate_limit = candidate_limit

    def getBestLabelSimilarity(self, source, target):
        best = 0.0
        has_token_overlap = len(source.tokens.intersection(target.tokens)) > 0

        for source_label in source.normalised_labels:
            for target_label in target.normalised_labels:
                if source_label == target_label:
                    best = max(best, 1.0)
                    continue

                isub_score = isub(source_label, target_label)
                token_score = jaccard(set(source_label.split()), set(target_label.split()))
                vector_score = cosineFromSets(characterNgrams(source_label), characterNgrams(target_label))

                if lev is not None:
                    jw_score = lev.jaro_winkler(source_label, target_label)
                else:
                    jw_score = 0.0

                score = max(isub_score, token_score, jw_score, vector_score)
                best = max(best, score)

        best = max(best, jaccard(source.tokens, target.tokens))
        if not has_token_overlap and best < 1.0:
            best = min(best, 0.80)
        return best

    def buildBlockingIndex(self, target_entities):
        index = defaultdict(list)
        prefix_index = defaultdict(list)

        for entity in target_entities:
            for token in entity.tokens:
                index[token].append(entity)
            if entity.local_name:
                prefix_index[entity.local_name[:1].lower()].append(entity)

        return index, prefix_index

    def getCandidateTargets(self, source, target_entities, index, prefix_index):
        candidates = []
        seen = set()

        for token in source.tokens:
            for target in index.get(token, []):
                if target.iri not in seen:
                    candidates.append(target)
                    seen.add(target.iri)

        if not candidates and source.local_name:
            candidates = prefix_index.get(source.local_name[:1].lower(), [])

        if not candidates:
            candidates = target_entities

        return candidates[: self.candidate_limit]

    def matchEntities(self, source_entities, target_entities, entity_type, threshold=None):
        if threshold is None:
            threshold = self.threshold

        mappings = []
        index, prefix_index = self.buildBlockingIndex(target_entities)

        for source in source_entities:
            best_mapping = None
            for target in self.getCandidateTargets(source, target_entities, index, prefix_index):
                if entity_type == "class" and "movie" in source.tokens and "movie" not in target.tokens:
                    continue
                score = self.getBestLabelSimilarity(source, target)
                if score >= threshold:
                    candidate = CandidateMapping(
                        source=source,
                        target=target,
                        entity_type=entity_type,
                        lexical_score=score,
                        final_score=score,
                    )
                    if best_mapping is None or candidate.final_score > best_mapping.final_score:
                        best_mapping = candidate

            if best_mapping is not None:
                mappings.append(best_mapping)

        return mappings
