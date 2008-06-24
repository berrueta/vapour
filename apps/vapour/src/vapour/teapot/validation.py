
from rdflib.Graph import ConjunctiveGraph
from rdflib.sparql.bison import Parse
from vapour.namespaces import *
from asserts import *
import socket

socket.setdefaulttimeout(5)

def validateRDF(graph, resourcesToCheck):
    for resource in resourcesToCheck:
        uri = resource["uri"]
        url = getFinalUrl(graph, uri)
        if (url != None):
            valid = validateRDFRepresentation(url, uri)
            #FIXME: it should be a different thing than a TestRequirement
            #testRequirement = addTestRequirement(graph, "Validating RDF representation of the vocabulary")
            #addAssertion(graph, vocabUri, RECIPES["TestValidRdfData"], validVocab, testRequirement)

def getFinalUrl(graph, uri):
    query= """
                SELECT ?url
                WHERE {
                    ?test dct:hasPart ?firstAssertion .
                    ?firstAssertion earl:subject ?firstSubject .
                    ?firstAssertion vapourv:previousSubject "HEAD" .
                    ?firstSubject earl:httpRequest ?firstRequest .
                    ?firstRequest uri:uri "%s" .
                    ?firstRequest http:accept "application/rdf+xml" .
                    ?test dct:hasPart ?lastAssertion .
                    ?lastAssertion earl:subject ?lastSubject .
                    ?lastSubject earl:httpRequest ?lastRequest .
                    ?lastResquest uri:uri ?url .
                    ?lastSubject earl:httpResponse ?lastResponse .
                    ?lastReponse http:responseCode "200" .
                }
            """ % uri 
    #FIXME: this query doesn't work
    results = graph.query(Parse(query), initNs=bindings).serialize('python')
    if (len(results)>0):
        return results[0]
    else:
        return None

def validateRDFRepresentation(url, uri):
    return (validateRDF(url) and validateRDFObject(url, uri))

def validateRDFContent(url):
    g = ConjunctiveGraph()
    try:
        g.parse(url)
    except Exception:
        return False
    return (len(g)>0)

def validateRDFObject(url, uri):
    g = ConjunctiveGraph()
    try:
        g.parse(url)
    except Exception:
        return False
    #len([x for x in graph.predicate_objects(uri)])
    bindings = { u"rdf":RDF }
    query = "SELECT ?type WHERE { <%s> rdf:type ?type }" % uri
    results = g.query(Parse(query), initNs=bindings).serialize('python')
    return (len(results)>0)

