from util import *
from vapour.namespaces import *
from rdflib import BNode

def assertLastResponseCode200(graph, rootTestSubject):
    testSubject = lastTestSubjectOfSequence(graph, rootTestSubject)
    result = (getResponseCode(graph, testSubject) == 200)
    addAssertion(graph, testSubject, RECIPES["TestResponseCode200"], result)
    
def assertIntermediateResponseCode303(graph, rootTestSubject):
    l = testSubjectsAsList(graph, rootTestSubject)
    for testSubject in l[0:len(l)-1]:
        result = (getResponseCode(graph, testSubject) == 303)
        addAssertion(graph, testSubject, RECIPES["TestResponseCode302"], result)
    
def assertLastResponseContentTypeRdf(graph, rootTestSubject):
    testSubject = lastTestSubjectOfSequence(graph, rootTestSubject)
    result = (getContentType(graph, testSubject) == "application/rdf+xml")
    addAssertion(graph, testSubject, RECIPES["TestContentTypeRdf"], result)

def getResponseCode(graph, testSubject):
    httpResponse = getHttpResponse(graph, testSubject)
    return int(getLiteralProperty(graph, httpResponse, HTTP["responseCode"]))

def getContentType(graph, testSubject):
    httpResponse = getHttpResponse(graph, testSubject)
    return str(getLiteralProperty(graph, httpResponse, HTTP["content-type"]))

def getHttpResponse(graph, testSubject):
    l = [x for x in graph.objects(testSubject, EARL["httpResponse"])]
    return l[0]

def getLiteralProperty(graph, resource, property):
    l = [x for x in graph.objects(resource, property)]
    if len(l) == 0: return None
    else: return l[0]
    
def addAssertion(graph, testSubject, test, validity):
    assertion = BNode()
    resultSubject = BNode()
    
    # link the nodes
    graph.add((assertion, EARL["result"], resultSubject))
        
    graph.add((assertion, RDF["type"], EARL["Assertion"]))
    graph.add((assertion, EARL["assertedBy"], VAPOUR_SOFT["vapour1-0"]))
    graph.add((assertion, EARL["subject"], testSubject));
    graph.add((assertion, EARL["mode"], EARL["automatic"]))
    graph.add((assertion, EARL["test"], test))
    
    graph.add((resultSubject, RDF["type"], EARL["TestResult"]))
    if (validity == True):
        validityResource = EARL["pass"]
    else:
        validityResource = EARL["fail"]
    graph.add((resultSubject, EARL["validity"], validityResource))
    
    return assertion
