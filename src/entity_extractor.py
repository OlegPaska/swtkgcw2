from dataclasses import dataclass, field
import re

from rdflib import Graph, URIRef
from rdflib.namespace import OWL, RDF, RDFS
from rdflib.util import guess_format


STOPWORDS = {
    "a", "an", "and", "by", "for", "has", "in", "is", "of", "on", "the", "to",
}


@dataclass
class OntologyEntity:
    iri: URIRef
    entity_type: str
    local_name: str
    labels: list[str] = field(default_factory=list)
    normalised_labels: list[str] = field(default_factory=list)
    tokens: set[str] = field(default_factory=set)
    parents: set[URIRef] = field(default_factory=set)
    children: set[URIRef] = field(default_factory=set)
    domains: set[URIRef] = field(default_factory=set)
    ranges: set[URIRef] = field(default_factory=set)
    rdf_types: set[URIRef] = field(default_factory=set)


def getLocalName(uri):
    uri_str = str(uri)
    if "#" in uri_str:
        return uri_str.rsplit("#", 1)[1]
    return uri_str.rstrip("/").rsplit("/", 1)[-1]


def splitCamelCase(text):
    text = re.sub(r"([a-z0-9])([A-Z])", r"\1 \2", text)
    text = re.sub(r"([A-Z]+)([A-Z][a-z])", r"\1 \2", text)
    return text


def normaliseLabel(label):
    label = splitCamelCase(str(label))
    label = label.replace("_", " ").replace("-", " ")
    label = re.sub(r"[^A-Za-z0-9 ]+", " ", label)
    label = re.sub(r"\s+", " ", label).strip().lower()
    return label


def tokeniseLabel(label):
    return {token for token in normaliseLabel(label).split() if token and token not in STOPWORDS}


class EntityExtractor(object):
    """
    Extracts ontology entities with a small rdflib-based API.

    The lab examples use owlready2 for entity access. rdflib is used here because
    it handles the local coursework Turtle/RDF files and OAEI mappings uniformly.
    """

    def __init__(self, ontology_file):
        self.ontology_file = ontology_file
        self.g = Graph()
        self.g.parse(ontology_file, format=guess_format(ontology_file))

    def getLabels(self, entity_uri):
        labels = [str(label) for label in self.g.objects(entity_uri, RDFS.label)]
        local_name = getLocalName(entity_uri)
        if local_name not in labels:
            labels.append(local_name)
        return labels

    def createEntity(self, entity_uri, entity_type):
        labels = self.getLabels(entity_uri)
        normalised = sorted({normaliseLabel(label) for label in labels if normaliseLabel(label)})
        tokens = set()
        for label in labels:
            tokens.update(tokeniseLabel(label))

        return OntologyEntity(
            iri=entity_uri,
            entity_type=entity_type,
            local_name=getLocalName(entity_uri),
            labels=labels,
            normalised_labels=normalised,
            tokens=tokens,
        )

    def extractClasses(self):
        entities = {}
        for class_type in [OWL.Class, RDFS.Class]:
            for cls in self.g.subjects(RDF.type, class_type):
                if isinstance(cls, URIRef):
                    entities[cls] = self.createEntity(cls, "class")

        for cls, parent in self.g.subject_objects(RDFS.subClassOf):
            if cls in entities and isinstance(parent, URIRef):
                entities[cls].parents.add(parent)
            if parent in entities and isinstance(cls, URIRef):
                entities[parent].children.add(cls)

        return list(entities.values())

    def extractProperties(self):
        entities = {}
        property_types = [OWL.ObjectProperty, OWL.DatatypeProperty, RDF.Property]
        for prop_type in property_types:
            for prop in self.g.subjects(RDF.type, prop_type):
                if isinstance(prop, URIRef):
                    entities[prop] = self.createEntity(prop, "property")

        for prop, parent in self.g.subject_objects(RDFS.subPropertyOf):
            if prop in entities and isinstance(parent, URIRef):
                entities[prop].parents.add(parent)
            if parent in entities and isinstance(prop, URIRef):
                entities[parent].children.add(prop)

        for prop, domain in self.g.subject_objects(RDFS.domain):
            if prop in entities and isinstance(domain, URIRef):
                entities[prop].domains.add(domain)

        for prop, range_value in self.g.subject_objects(RDFS.range):
            if prop in entities and isinstance(range_value, URIRef):
                entities[prop].ranges.add(range_value)

        return list(entities.values())

    def extractIndividuals(self):
        class_iris = {entity.iri for entity in self.extractClasses()}
        property_iris = {entity.iri for entity in self.extractProperties()}
        schema_iris = class_iris.union(property_iris)

        entities = {}
        for subject, rdf_type in self.g.subject_objects(RDF.type):
            if not isinstance(subject, URIRef):
                continue
            if subject in schema_iris:
                continue
            if rdf_type in {
                OWL.Class,
                RDFS.Class,
                OWL.ObjectProperty,
                OWL.DatatypeProperty,
                OWL.AnnotationProperty,
                RDF.Property,
                OWL.Ontology,
            }:
                continue

            if subject not in entities:
                entities[subject] = self.createEntity(subject, "individual")
            if isinstance(rdf_type, URIRef):
                entities[subject].rdf_types.add(rdf_type)

        return list(entities.values())

    def extractAll(self):
        return {
            "classes": self.extractClasses(),
            "properties": self.extractProperties(),
            "individuals": self.extractIndividuals(),
        }
