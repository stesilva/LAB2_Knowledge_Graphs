from rdflib import Graph
import owlrl

g = Graph()
g.parse("12L-GomesYerbolatova/assets/12L-B1-GomesYerbolatova.ttl", format="turtle")
g.parse("12L-GomesYerbolatova/assets/12L-B2-GomesYerbolatova.ttl", format="turtle")

#Activate inference (OWL RL reasoning)
owlrl.DeductiveClosure(owlrl.OWLRL_Semantics).expand(g)


'''List all persons who work on determined paper
  - should return all authors, corresponded_author and reviewers (should not return event chair or journal editor)
  - use subClassOf concept to find the persons
'''

query_01 = """
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX rp: <http://www.example.edu/research-publication/>

SELECT DISTINCT ?person ?person_name ?role ?paper
WHERE {
  #Find all subclasses of rp:person except event_chair and journal_editor
  ?role rdfs:subClassOf rp:person .
  FILTER (?role != rp:event_chair && ?role != rp:journal_editor)
  
  #Find persons of those roles
  ?person a ?role .
  OPTIONAL { ?person rp:person_name ?person_name }
  
  #Find persons linked to the determined paper by authoring, corresponding, or reviewing
  ?paper a rp:paper .
  {
    ?person rp:wrote ?paper .
  }
  UNION
  {
    ?person rp:corresponded ?paper .
  }
  UNION
  {
    ?person rp:reviewed ?paper .
  }
  
  #Filter by paper ID
  #FILTER (?paper = <http://www.example.edu/research-publication/paper/37d616207b242f7ab072225f1bba26b8c33c7c99>)
}
"""

for row in g.query(query_01):
  print(f"Person: {row.person}, Name: {row.person_name}, Role: {row.role}, Paper: {row.paper}")



'''Find all papers that both cite other papers and are themselves cited by other papers
    - These papers are active nodes in the citation network: they are both consumers and producers of scholarly influence. 
      They may represent important or foundational works that are engaged in ongoing scholarly dialogue.

    - Work with domain and range where a class is at the same the domain and the range
'''

query_02 = """
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX rp: <http://www.example.edu/research-publication/>

SELECT DISTINCT ?paper
WHERE {
  ?paper rdf:type rp:paper .
  ?paper rp:cites ?otherPaper . #paper as domain
  ?citingPaper rp:cites ?paper . #paper as range
}
"""

for row in g.query(query_02):
    print(f"Active Paper: {row.paper}")
