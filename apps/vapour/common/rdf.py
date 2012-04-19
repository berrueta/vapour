
def performSparqlQuery(graph, query, lib="rdflib"):
    if (lib == "rdflib" ):
        return performSparqlQueryRdfLib(graph, query)
    else:
        return performSparqlQueryLibRdf(graph, query)

def performSparqlQueryLibRdf(graph, query):
    import RDF
    from vapour.namespaces import buildPrefixesSparqlDeclaration
    query = normalizeQuery(buildPrefixesSparqlDeclaration() + query)
    #loggger.debug("Performing SPARQL query: %s" % query)
    parser = RDF.Parser(mime_type="application/rdf+xml")
    model = RDF.Model()
    parser.parse_string_into_model(model, graph.serialize(format="xml"), "http://validator.linkeddata.org/vapour")
    if type(query) is unicode: 
        query = query.encode("utf-8") # http://bugs.librdf.org/mantis/view.php?id=464
    q = RDF.Query(query, query_language="sparql")
    vars = getQueryVars(query)
    #loggger.debug("Vars: %s (%d)" % (vars, len(vars)))
    results = []
    for row in q.execute(model):
        result = []
        for var in vars:
            if (row[var]):
                result.append(getLibRdfNodeValue(row[var]))
            else:
                result.append(None)
        results.append(result)
    #loggger.debug("Returned %d results" % len(results))
    return results

def performSparqlQueryRdfLib(graph, query):
    import rdflib
    rdflib.plugin.register("sparql", rdflib.query.Processor, "rdfextras.sparql.processor", "Processor")
    rdflib.plugin.register("sparql", rdflib.query.Result, "rdfextras.sparql.query", "SPARQLQueryResult")
    from vapour.namespaces import bindings
    #loggger.debug("Performing SPARQL query: %s" % normalizeQuery(query))
    results = graph.query(query, initNs=bindings)
    #loggger.debug("Returned %d results" % len(results))
    return results

def normalizeQuery(query):
    for string in ["\n","\t","           ","          ","         ","         ","        ","       ","      ","     ","    ","   ","  "]: #FIXME: regex
        query = query.replace(string, " ")
    return query

def getQueryVars(query):
    import re
    p = re.compile("select (distinct )?((\?[a-zA-Z]+ )+)where*", re.IGNORECASE)
    m = p.search(query)
    vars = []
    if (m):
        for var in m.groups()[1].strip().split(" "):
            vars.append(var[1:])
    return vars

def getLibRdfNodeValue(node):
    if node.is_resource():
        return str(node.uri)
    elif node.is_blank():
        return node.blank_identifier
    elif node.is_literal():
        if (str(node.literal_value["datatype"]) == "http://www.w3.org/2001/XMLSchema#integer"):
            return int(node.literal_value["string"])
        else:
            return node.literal_value["string"]
    else:
        return str(node)

