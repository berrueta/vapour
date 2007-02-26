from util import *
from vapour.namespaces import *
from rdflib import BNode

def assertLastResponseCode200(graph, rootTestSubject):
    testSubject = lastTestSubjectOfSequence(graph, rootTestSubject)
    # FIXME
    # suppose that the test passes...
    addAssertion(graph, testSubject, RECIPES["TestResponseCode200"], True)
    
def assertIntermediateResponseCode303(graph, rootTestSubject):
    # FIXME
    None
    
def assertLastResponseContentTypeRdf(graph, rootTestSubject):
    testSubject = lastTestSubjectOfSequence(graph, rootTestSubject)
    # FIXME
    
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
