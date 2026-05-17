def setOverlapScore(values1, values2):
    if not values1 or not values2:
        return 0.0
    return len(values1.intersection(values2)) / len(values1.union(values2))


class StructuralMatcher(object):
    def __init__(self, structural_weight=0.15):
        self.structural_weight = structural_weight

    def getStructuralScore(self, mapping):
        source = mapping.source
        target = mapping.target

        parent_score = setOverlapScore(source.parents, target.parents)
        child_score = setOverlapScore(source.children, target.children)
        domain_score = setOverlapScore(source.domains, target.domains)
        range_score = setOverlapScore(source.ranges, target.ranges)
        type_score = setOverlapScore(source.rdf_types, target.rdf_types)

        return max(parent_score, child_score, domain_score, range_score, type_score)

    def rerankMappings(self, mappings):
        for mapping in mappings:
            mapping.structural_score = self.getStructuralScore(mapping)
            mapping.final_score = (
                (1.0 - self.structural_weight) * mapping.lexical_score
                + self.structural_weight * mapping.structural_score
            )
        return mappings

