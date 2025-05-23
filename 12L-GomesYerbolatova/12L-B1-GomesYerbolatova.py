from rdflib import Graph, Namespace
from rdflib.namespace import RDF, RDFS, XSD

#define a custom namespace
rp = Namespace("http://www.rpample.edu/research-publication/")

#create a new graph
g = Graph()

#binding prefixes to namespaces
g.bind("rp", rp)
g.bind("rdf", RDF)
g.bind("rdfs", RDFS)
g.bind("xsd", XSD)

#classes
g.add((rp.person, RDF.type, RDFS.Class))
g.add((rp.author, RDF.type, RDFS.Class))
g.add((rp.reviewer, RDF.type, RDFS.Class))
g.add((rp.journalEditor, RDF.type, RDFS.Class))
g.add((rp.eventChair, RDF.type, RDFS.Class))
g.add((rp.paper, RDF.type, RDFS.Class))
g.add((rp.keyword, RDF.type, RDFS.Class))
g.add((rp.publication, RDF.type, RDFS.Class))
g.add((rp.journal, RDF.type, RDFS.Class))
g.add((rp.event, RDF.type, RDFS.Class))
g.add((rp.edition, RDF.type, RDFS.Class))
g.add((rp.volume, RDF.type, RDFS.Class))
g.add((rp.conference, RDF.type, RDFS.Class))
g.add((rp.workshop, RDF.type, RDFS.Class))
g.add((rp.editionYear, RDF.type, RDFS.Class))
g.add((rp.editionCity, RDF.type, RDFS.Class))
g.add((rp.volumeYear, RDF.type, RDFS.Class))

#subclass
g.add((rp.author, RDFS.subClassOf, rp.person))
g.add((rp.reviewer, RDFS.subClassOf, rp.person))
g.add((rp.journalEditor, RDFS.subClassOf, rp.person))
g.add((rp.eventChair, RDFS.subClassOf, rp.person))
g.add((rp.conference, RDFS.subClassOf, rp.event))
g.add((rp.workshop, RDFS.subClassOf, rp.event))

#Properties (literal, class)
#Person properties
g.add((rp.personName, RDF.type, RDF.Property))
g.add((rp.personName, RDFS.domain, rp.person))
g.add((rp.personName, RDFS.range, XSD.string))

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

#Edition properties
g.add((rp.editionNumber, RDF.type, RDF.Property))
g.add((rp.editionNumber, RDFS.domain, rp.edition))
g.add((rp.editionNumber, RDFS.range, XSD.integer))

g.add((rp.hasEditionYear, RDF.type, RDF.Property))
g.add((rp.hasEditionYear, RDFS.domain, rp.edition))
g.add((rp.hasEditionYear, RDFS.range, rp.editionYear))

g.add((rp.hasEditionCity, RDF.type, RDF.Property))
g.add((rp.hasEditionCity, RDFS.domain, rp.edition))
g.add((rp.hasEditionCity, RDFS.range, rp.editionCity))

#Volume properties
g.add((rp.volumeNumber, RDF.type, RDF.Property))
g.add((rp.volumeNumber, RDFS.domain, rp.volume))
g.add((rp.volumeNumber, RDFS.range, XSD.integer))

g.add((rp.hasVolumeYear, RDF.type, RDF.Property))
g.add((rp.hasVolumeYear, RDFS.domain, rp.volume))
g.add((rp.hasVolumeYear, RDFS.range, rp.volumeYear))

#Event properties
g.add((rp.eventURL, RDF.type, RDF.Property))
g.add((rp.eventURL, RDFS.domain, rp.event))
g.add((rp.eventURL, RDFS.range, XSD.string))

g.add((rp.eventName, RDF.type, RDF.Property))
g.add((rp.eventName, RDFS.domain, rp.event))
g.add((rp.eventName, RDFS.range, XSD.string))

g.add((rp.hasChair, RDF.type, RDF.Property))
g.add((rp.hasChair, RDFS.domain, rp.event))
g.add((rp.hasChair, RDFS.range, rp.eventChair))

g.add((rp.hasEdition, RDF.type, RDF.Property))
g.add((rp.hasEdition, RDFS.domain, rp.event))
g.add((rp.hasEdition, RDFS.range, rp.edition))

#Journal properties
g.add((rp.journalURL, RDF.type, RDF.Property))
g.add((rp.journalURL, RDFS.domain, rp.journal))
g.add((rp.journalURL, RDFS.range, XSD.string))

g.add((rp.journalName, RDF.type, RDF.Property))
g.add((rp.journalName, RDFS.domain, rp.journal))
g.add((rp.journalName, RDFS.range, XSD.string))

g.add((rp.issn, RDF.type, RDF.Property))
g.add((rp.issn, RDFS.domain, rp.journal))
g.add((rp.issn, RDFS.range, XSD.string))

g.add((rp.hasJournalEditor, RDF.type, RDF.Property))
g.add((rp.hasJournalEditor, RDFS.domain, rp.journal))
g.add((rp.hasJournalEditor, RDFS.range, rp.journalEditor))

g.add((rp.hasVolume, RDF.type, RDF.Property))
g.add((rp.hasVolume, RDFS.domain, rp.journal))
g.add((rp.hasVolume, RDFS.range, rp.volume))

#Relationships
g.add((rp.hasKeyword, RDF.type, RDF.Property))
g.add((rp.hasKeyword, RDFS.domain, rp.paper))
g.add((rp.hasKeyword, RDFS.range, rp.keyword))

g.add((rp.cites, RDF.type, RDF.Property))
g.add((rp.cites, RDFS.domain, rp.paper))
g.add((rp.cites, RDFS.range, rp.paper))

g.add((rp.published, RDF.type, RDF.Property))
g.add((rp.published, RDFS.domain, rp.publication))
g.add((rp.published, RDFS.range, rp.paper))

g.add((rp.publishedInEdition, RDF.type, RDF.Property))
g.add((rp.publishedInEdition, RDFS.domain, rp.publication))
g.add((rp.publishedInEdition, RDFS.range, rp.edition))

g.add((rp.publishedInVolume, RDF.type, RDF.Property))
g.add((rp.publishedInVolume, RDFS.domain, rp.publication))
g.add((rp.publishedInVolume, RDFS.range, rp.volume))

g.add((rp.wrote, RDF.type, RDF.Property))
g.add((rp.wrote, RDFS.domain, rp.author))
g.add((rp.wrote, RDFS.range, rp.paper))

g.add((rp.corresponded, RDF.type, RDF.Property))
g.add((rp.corresponded, RDFS.domain, rp.author))
g.add((rp.corresponded, RDFS.range, rp.paper))

g.add((rp.reviewed, RDF.type, RDF.Property))
g.add((rp.reviewed, RDFS.domain, rp.reviewer))
g.add((rp.reviewed, RDFS.range, rp.paper))

g.add((rp.assignsForEvent, RDF.type, RDF.Property))
g.add((rp.assignsForEvent, RDFS.domain, rp.eventChair))
g.add((rp.assignsForEvent, RDFS.range, rp.reviewer))

g.add((rp.assignsForJournal, RDF.type, RDF.Property))
g.add((rp.assignsForJournal, RDFS.domain, rp.journalEditor))
g.add((rp.assignsForJournal, RDFS.range, rp.reviewer))

#subProperty
g.add((rp.corresponded, RDFS.subPropertyOf, rp.wrote))

#serialize to turtle format
g.serialize(destination='12L-GomesYerbolatova/assets/12L-B1-GomesYerbolatova.ttl', format='turtle')