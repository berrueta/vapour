
from rdflib.graph import ConjunctiveGraph
from vapour.common.rdf import performSparqlQuery
from vapour.namespaces import RECIPES
from asserts import addAssertion
from util import *
import httplib
from StringIO import StringIO

def assertLastResponseBodyContainsDefinitionForResource(graph, resource, httpResponse, rootTestSubject, testRequirement):
    testSubject = lastTestSubjectOfSequence(graph, rootTestSubject)
    if getResponseCode(graph, testSubject) == httplib.OK:
        body = httpResponse.read()
        g = ConjunctiveGraph()
        try:
            g.parse(StringIO(body), getRequestUri(graph, testSubject))
            addAssertion(graph, testSubject, RECIPES["TestResponseParseableRdf"], True, testRequirement)
        except Exception, e:
            addAssertion(graph, testSubject, RECIPES["TestResponseParseableRdf"], False, testRequirement)
            return False
        query = "SELECT * WHERE { <%s> ?p ?o }" % resource['uri']
        definitionTriples = performSparqlQuery(g, query)
#        definitionTriples = [(p,o) for (p,o) in g.predicate_objects(resource)]
        isThereADefinitionForTheResource = len(definitionTriples) > 0
        addAssertion(graph, testSubject, RECIPES["TestContainsResourceDefinition"], isThereADefinitionForTheResource, testRequirement)
        return isThereADefinitionForTheResource
