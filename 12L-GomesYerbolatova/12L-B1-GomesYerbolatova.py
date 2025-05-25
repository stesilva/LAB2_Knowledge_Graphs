from rdflib import Graph, Namespace
from rdflib.namespace import RDF, RDFS, XSD

#define a custom _namespace
rp = Namespace("http://www.example.edu/research-publication/")

#create a new graph
g = Graph()

#binding prefixes to _namespaces
g.bind("rp", rp)
g.bind("rdf", RDF)
g.bind("rdfs", RDFS)
g.bind("xsd", XSD)

#classes
g.add((rp.person, RDF.type, RDFS.Class))
g.add((rp.author, RDF.type, RDFS.Class))
g.add((rp.reviewer, RDF.type, RDFS.Class))
g.add((rp.journal_editor, RDF.type, RDFS.Class))
g.add((rp.event_chair, RDF.type, RDFS.Class))
g.add((rp.paper, RDF.type, RDFS.Class))
g.add((rp.keyword, RDF.type, RDFS.Class))
g.add((rp.publication, RDF.type, RDFS.Class))
g.add((rp.journal, RDF.type, RDFS.Class))
g.add((rp.event, RDF.type, RDFS.Class))
g.add((rp.edition, RDF.type, RDFS.Class))
g.add((rp.volume, RDF.type, RDFS.Class))
g.add((rp.conference, RDF.type, RDFS.Class))
g.add((rp.workshop, RDF.type, RDFS.Class))
g.add((rp.edition_year, RDF.type, RDFS.Class))
g.add((rp.edition_city, RDF.type, RDFS.Class))
g.add((rp.volume_year, RDF.type, RDFS.Class))

#subclass
g.add((rp.author, RDFS.subClassOf, rp.person))
g.add((rp.reviewer, RDFS.subClassOf, rp.person))
g.add((rp.journal_editor, RDFS.subClassOf, rp.person))
g.add((rp.event_chair, RDFS.subClassOf, rp.person))
g.add((rp.conference, RDFS.subClassOf, rp.event))
g.add((rp.workshop, RDFS.subClassOf, rp.event))

#Properties (literal, class)
#Person properties
g.add((rp.person_name, RDF.type, RDF.Property))
g.add((rp.person_name, RDFS.domain, rp.person))
g.add((rp.person_name, RDFS.range, XSD.string))

#Paper properties
g.add((rp.title, RDF.type, RDF.Property))
g.add((rp.title, RDFS.domain, rp.paper))
g.add((rp.title, RDFS.range, XSD.string))

g.add((rp.abstract, RDF.type, RDF.Property))
g.add((rp.abstract, RDFS.domain, rp.paper))
g.add((rp.abstract, RDFS.range, XSD.string))

#Publication properties
g.add((rp.pages, RDF.type, RDF.Property))
g.add((rp.pages, RDFS.domain, rp.publication))
g.add((rp.pages, RDFS.range, XSD.string))

#_edition properties
g.add((rp.edition_number, RDF.type, RDF.Property))
g.add((rp.edition_number, RDFS.domain, rp.edition))
g.add((rp.edition_number, RDFS.range, XSD.integer))

g.add((rp.has_edition_year, RDF.type, RDF.Property))
g.add((rp.has_edition_year, RDFS.domain, rp.edition))
g.add((rp.has_edition_year, RDFS.range, rp.edition_year))

g.add((rp.has_edition_city, RDF.type, RDF.Property))
g.add((rp.has_edition_city, RDFS.domain, rp.edition))
g.add((rp.has_edition_city, RDFS.range, rp.edition_city))

#Volume properties
g.add((rp.volume_number, RDF.type, RDF.Property))
g.add((rp.volume_number, RDFS.domain, rp.volume))
g.add((rp.volume_number, RDFS.range, XSD.integer))

g.add((rp.has_volume_year, RDF.type, RDF.Property))
g.add((rp.has_volume_year, RDFS.domain, rp.volume))
g.add((rp.has_volume_year, RDFS.range, rp.volume_year))

#Event properties
g.add((rp.event_url, RDF.type, RDF.Property))
g.add((rp.event_url, RDFS.domain, rp.event))
g.add((rp.event_url, RDFS.range, XSD.string))

g.add((rp.event_name, RDF.type, RDF.Property))
g.add((rp.event_name, RDFS.domain, rp.event))
g.add((rp.event_name, RDFS.range, XSD.string))

g.add((rp.has_chair, RDF.type, RDF.Property))
g.add((rp.has_chair, RDFS.domain, rp.event))
g.add((rp.has_chair, RDFS.range, rp.event_chair))

g.add((rp.has_edition, RDF.type, RDF.Property))
g.add((rp.has_edition, RDFS.domain, rp.event))
g.add((rp.has_edition, RDFS.range, rp.edition))

#Journal properties
g.add((rp.journal_url, RDF.type, RDF.Property))
g.add((rp.journal_url, RDFS.domain, rp.journal))
g.add((rp.journal_url, RDFS.range, XSD.string))

g.add((rp.journal_name, RDF.type, RDF.Property))
g.add((rp.journal_name, RDFS.domain, rp.journal))
g.add((rp.journal_name, RDFS.range, XSD.string))

g.add((rp.ISSN, RDF.type, RDF.Property))
g.add((rp.ISSN, RDFS.domain, rp.journal))
g.add((rp.ISSN, RDFS.range, XSD.string))

g.add((rp.has_journal_editor, RDF.type, RDF.Property))
g.add((rp.has_journal_editor, RDFS.domain, rp.journal))
g.add((rp.has_journal_editor, RDFS.range, rp.journal_editor))

g.add((rp.has_volume, RDF.type, RDF.Property))
g.add((rp.has_volume, RDFS.domain, rp.journal))
g.add((rp.has_volume, RDFS.range, rp.volume))

#Relationships
g.add((rp.has_keyword, RDF.type, RDF.Property))
g.add((rp.has_keyword, RDFS.domain, rp.paper))
g.add((rp.has_keyword, RDFS.range, rp.keyword))

g.add((rp.cites, RDF.type, RDF.Property))
g.add((rp.cites, RDFS.domain, rp.paper))
g.add((rp.cites, RDFS.range, rp.paper))

g.add((rp.published, RDF.type, RDF.Property))
g.add((rp.published, RDFS.domain, rp.publication))
g.add((rp.published, RDFS.range, rp.paper))

g.add((rp.published_in_edition, RDF.type, RDF.Property))
g.add((rp.published_in_edition, RDFS.domain, rp.publication))
g.add((rp.published_in_edition, RDFS.range, rp.edition))

g.add((rp.published_in_volume, RDF.type, RDF.Property))
g.add((rp.published_in_volume, RDFS.domain, rp.publication))
g.add((rp.published_in_volume, RDFS.range, rp.volume))

g.add((rp.wrote, RDF.type, RDF.Property))
g.add((rp.wrote, RDFS.domain, rp.author))
g.add((rp.wrote, RDFS.range, rp.paper))

g.add((rp.corresponded, RDF.type, RDF.Property))
g.add((rp.corresponded, RDFS.domain, rp.author))
g.add((rp.corresponded, RDFS.range, rp.paper))

g.add((rp.reviewed, RDF.type, RDF.Property))
g.add((rp.reviewed, RDFS.domain, rp.reviewer))
g.add((rp.reviewed, RDFS.range, rp.paper))

g.add((rp.assigns_for_event, RDF.type, RDF.Property))
g.add((rp.assigns_for_event, RDFS.domain, rp.event_chair))
g.add((rp.assigns_for_event, RDFS.range, rp.reviewer))

g.add((rp.assigns_for_journal, RDF.type, RDF.Property))
g.add((rp.assigns_for_journal, RDFS.domain, rp.journal_editor))
g.add((rp.assigns_for_journal, RDFS.range, rp.reviewer))

#subProperty
g.add((rp.corresponded, RDFS.subPropertyOf, rp.wrote))

#serialize to turtle format
g.serialize(destination='12L-GomesYerbolatova/assets/12L-B1-GomesYerbolatova.ttl', format='turtle')