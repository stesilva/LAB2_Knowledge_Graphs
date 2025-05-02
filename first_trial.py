from SPARQLWrapper import SPARQLWrapper, JSON

sparql = SPARQLWrapper("http://LAPTOP-BC44NPR8:7200/repositories/DBPEDIA")
sparql.setQuery("""
    SELECT DISTINCT ?s WHERE {
        ?s ?p ?o .
    } LIMIT 10
""")
sparql.setReturnFormat(JSON)
results = sparql.query().convert()

for result in results["results"]["bindings"]:
    print(result["s"]["value"])
