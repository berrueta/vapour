
from rdflib.Graph import ConjunctiveGraph
from rdflib.sparql.bison import Parse
from vapour.namespaces import *
from asserts import *
import socket

socket.setdefaulttimeout(5)

def validateRDF(graph, vocabUri, classUri, propertyUri):
    vocabUrl = getFinalUrl(graph, vocabUri)
    validVocab = validateRDFContent(vocabUrl)
    #testRequirement = addTestRequirement(graph, "Validating RDF representation of the vocabulary")
    #addAssertion(graph, vocabUri, RECIPES["TestValidRdfData"], validVocab, testRequirement)
    
    classUrl = getFinalUrl(graph, classUri)
    validClass = validateRDFContent(classUrl) and validateUri(classUrl, classUri)
    #testRequirement = addTestRequirement(graph, "Validating definition of the resource " + str(classUri))
    #addAssertion(graph, classUri, RECIPES["TestContainsResourceDefinition"], validClass, testRequirement)
    
    propertyUrl = getFinalUrl(graph, propertyUri)
    validProperty = validateRDFContent(propertyUrl) and validateUri(propertyUrl, propertyUri)
    #testRequirement = addTestRequirement(graph, "Validating definition of the resource " + str(propertyUri))
    #addAssertion(graph, propertyUri, RECIPES["TestContainsResourceDefinition"], validProperty, testRequirement)

def getFinalUrl(graph, uri):
    bindings = { u"dct":DCT, u"earl":EARL, u"uri":URI }
    query = """
                SELECT ?url 
                WHERE {
                    <%s> dct:hasPart ?assertion .
                    ?assertion earl:subject ?testSubject .
                    ?testSubject earl:httpRequest ?getRequest .
                    ?getRequest uri:uri ?url
                }
            """ % uri
    results = graph.query(Parse(query), initNs=bindings).serialize('python')
    if (len(results)>0):
        return results[0]
    else:
        return None

def validateRDFContent(url):
    graph = ConjunctiveGraph()
    try:
        graph.parse(url)
    except Exception:
        return False
    return (len(graph)>0)

def validateUri(url, uri):
    graph = ConjunctiveGraph()
    try:
        graph.parse(url)
    except Exception:
        return False
    #len([x for x in graph.predicate_objects(uri)])
    bindings = { u"rdf":RDF }
    query = "SELECT ?type WHERE { <%s> rdf:type ?type }" % uri
    results = graph.query(Parse(query), initNs=bindings).serialize('python')
    return (len(results)>0)

