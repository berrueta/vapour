
import rdflib
rdflib.plugin.register("sparql", rdflib.query.Processor, "rdfextras.sparql.processor", "Processor")
rdflib.plugin.register("sparql", rdflib.query.Result, "rdfextras.sparql.query", "SPARQLQueryResult")
from vapour.namespaces import bindings
from vapour.cup.common import createLogger

def performSparqlQuery(graph, query):
    logger = createLogger()
    logger.debug("Performing SPARQL query: %s" % normalizeQuery(query))
    results = graph.query(query, initNs=bindings)
    logger.debug("Returned %d results" % len(results))
    return results

def normalizeQuery(query):
    for string in ["\n","\t","  ","   ","    ","     ","      ","       ","        ","         ","         ","          ","           "]: #FIXME: regex
        query = query.replace(string, " ")
    return query
