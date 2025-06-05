from rdflib import Graph
import owlrl

g = Graph()
g.parse("12L-GomesYerbolatova/assets/12L-B1-GomesYerbolatova.ttl", format="turtle")
g.parse("12L-GomesYerbolatova/assets/12L-B2-GomesYerbolatova.ttl", format="turtle")

#Activate inference (OWL RL reasoning)
owlrl.DeductiveClosure(owlrl.OWLRL_Semantics).expand(g)


'''Cross-Domain Research Impact Analysis with Reasoning
It counts the papers that people wrote, corresponded and reviewed and calculates based 
on that their influence scores + gets keywords of their papers (domain of authors)
This query leverages the T-Box class hierarchy to find influential researchers who span
multiple roles in the academic ecosystem. It demonstrates reasoning over the person superclass
'''

query_01 = """
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX rp: <http://www.example.edu/research-publication/>
PREFIX rdfs: <http://www.rdfs.org/2000/01/rdf-schema#>

SELECT ?personName ?authorPapers ?correspondedPapers ?reviewedPapers ?totalInfluence
       (GROUP_CONCAT(DISTINCT STRAFTER(STR(?keyword), "/keyword/"); separator=", ") AS ?researchAreas)
WHERE {
    # Find persons who are both authors and reviewers (multi-role academics)
    ?person a rp:person ;
            rp:person_name ?personName .
    
    # Count papers they authored (includes corresponded papers via subproperty reasoning)
    {
        SELECT ?person (COUNT(DISTINCT ?authoredPaper) AS ?authorPapers) WHERE {
            ?person rp:wrote ?authoredPaper .
        }
        GROUP BY ?person
    }
    
    # Count papers they corresponded for (demonstrates subproperty reasoning)
    OPTIONAL {
        SELECT ?person (COUNT(DISTINCT ?correspondedPaper) AS ?correspondedPapers) WHERE {
            ?person rp:corresponded ?correspondedPaper .
        }
        GROUP BY ?person
    }
    
    # Count papers they reviewed (cross-role analysis)
    OPTIONAL {
        SELECT ?person (COUNT(DISTINCT ?reviewedPaper) AS ?reviewedPapers) WHERE {
            ?person rp:reviewed ?reviewedPaper .
        }
        GROUP BY ?person
    }
    
    # Get research areas from authored papers
    OPTIONAL {
        ?person rp:wrote ?paper .
        ?paper rp:has_keyword ?keywordURI .
        # Extract keyword from URI (assumes keyword is in URI fragment)
        BIND(REPLACE(STR(?keywordURI), ".[/#]([^/#])$", "$1") AS ?keyword)
    }
    
    # Calculate total influence score
		BIND(
            (COALESCE(?authorPapers, 0) * 1) + 
            (COALESCE(?correspondedPapers, 0) * 2) + 
            (COALESCE(?reviewedPapers, 0) * 3) 
        AS ?totalInfluence)
    
    # Filter for influential multi-role academics
    FILTER(?totalInfluence > 2)
}
GROUP BY ?personName ?authorPapers ?correspondedPapers ?reviewedPapers ?totalInfluence
ORDER BY DESC(?totalInfluence) ?personName
LIMIT 10
"""

'''Multi-Venue Cross-Citation Analysis with Subclass Reasoning
This query leverages the TBOX class hierarchy (conference and workshop as subclasses of event)
to analyze citation patterns across different types of publication venues, identifying authors who
publish across multiple venue types and cite each other's work.
Subclass reasoning: Uses rdfs:subClassOf* to automatically include both conferences and workshops when querying for events
Complex relationship traversal: Follows multiple relationship paths (author→paper→publication→venue)
Cross-venue analysis: Identifies interdisciplinary citation patterns that span different publication types
'''

query_02 = """
PREFIX rp: <http://www.example.edu/research-publication/>
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>

SELECT ?author_name ?citing_venue_type ?cited_venue_type 
       (COUNT(DISTINCT ?citing_paper) AS ?papers_citing) 
       (COUNT(DISTINCT ?cited_paper) AS ?papers_cited)
       (COUNT(DISTINCT ?citation_link) AS ?total_citations)
WHERE {
  # Find authors who wrote papers
  ?author rp:wrote ?citing_paper .
  ?author rp:person_name ?author_name .
  
  # These papers cite other papers
  ?citing_paper rp:cites ?cited_paper .
  BIND(CONCAT(STR(?citing_paper), "-", STR(?cited_paper)) AS ?citation_link)
  
  # Find venue types for citing papers (using reasoning but filtering out parent class)
  {
    ?pub1 rp:published ?citing_paper .
    ?pub1 rp:published_in_edition ?edition1 .
    ?venue1 rp:has_edition ?edition1 .
    ?venue1 rdf:type ?venue_type1 .
    ?venue_type1 rdfs:subClassOf* rp:event .
    # Filter out the parent 'event' class to get only specific subtypes
    FILTER(?venue_type1 != rp:event)
    BIND(STRAFTER(STR(?venue_type1), STR(rp:)) AS ?citing_venue_type)
  }
  UNION
  {
    ?pub1 rp:published ?citing_paper .
    ?pub1 rp:published_in_volume ?volume1 .
    BIND("journal" AS ?citing_venue_type)
  }
  
  # Find venue types for cited papers (using reasoning but filtering out parent class)
  {
    ?pub2 rp:published ?cited_paper .
    ?pub2 rp:published_in_edition ?edition2 .
    ?venue2 rp:has_edition ?edition2 .
    ?venue2 rdf:type ?venue_type2 .
    ?venue_type2 rdfs:subClassOf* rp:event .
    # Filter out the parent 'event' class to get only specific subtypes
    FILTER(?venue_type2 != rp:event)
    BIND(STRAFTER(STR(?venue_type2), STR(rp:)) AS ?cited_venue_type)
  }
  UNION
  {
    ?pub2 rp:published ?cited_paper .
    ?pub2 rp:published_in_volume ?volume2 .
    BIND("journal" AS ?cited_venue_type)
  }
  
  # Filter for cross-venue citations (different venue types)
  FILTER(?citing_venue_type != ?cited_venue_type)
}
GROUP BY ?author_name ?citing_venue_type ?cited_venue_type
HAVING (COUNT(DISTINCT ?citation_link) >= 2)
ORDER BY DESC(?total_citations)?author_name
"""


