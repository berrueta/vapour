
from util import *
from vapour.namespaces import *
from rdflib import BNode, Literal, URIRef
import mimetypes

reqCount = 1

def assertLastResponseCode200(graph, rootTestSubject, testRequirement):
    testSubject = lastTestSubjectOfSequence(graph, rootTestSubject)
    result = (getResponseCode(graph, testSubject) == 200)
    addAssertion(graph, testSubject, RECIPES["TestResponseCode200"], result, testRequirement)
    
def assertIntermediateResponseCode303(graph, rootTestSubject, testRequirement):
    l = testSubjectsAsList(graph, rootTestSubject)
    for testSubject in l[0:len(l)-1]:
        result = (getResponseCode(graph, testSubject) == 303)
        addAssertion(graph, testSubject, RECIPES["TestResponseCode303"], result, testRequirement)

def assertLastResponseContentTypeHtml(graph, rootTestSubject, testRequirement):
    testSubject = lastTestSubjectOfSequence(graph, rootTestSubject)
    result = (mimetypes.html in getContentType(graph, testSubject))
    addAssertion(graph, testSubject, RECIPES["TestContentTypeHtml"], result, testRequirement)
    
def assertLastResponseContentTypeXhtml(graph, rootTestSubject, testRequirement):
    testSubject = lastTestSubjectOfSequence(graph, rootTestSubject)
    result = (mimetypes.xhtml in getContentType(graph, testSubject))
    addAssertion(graph, testSubject, RECIPES["TestContentTypeXhtml"], result, testRequirement)
    
def assertLastResponseContentTypeXhtmlOrHtml(graph, rootTestSubject, testRequirement):
    testSubject = lastTestSubjectOfSequence(graph, rootTestSubject)
    result = (mimetypes.xhtml in getContentType(graph, testSubject)) or (mimetypes.html in getContentType(graph, testSubject))
    addAssertion(graph, testSubject, RECIPES["TestContentTypeXhtmlOrHtml"], result, testRequirement)
    
def assertLastResponseContentTypeRdf(graph, rootTestSubject, testRequirement):
    testSubject = lastTestSubjectOfSequence(graph, rootTestSubject)
    result = (mimetypes.rdfXml in getContentType(graph, testSubject))
    addAssertion(graph, testSubject, RECIPES["TestContentTypeRdf"], result, testRequirement)

def assertVaryHeader(graph, testSubject, validity, testRequirement):
    addAssertion(graph, testSubject, RECIPES["TestResponseContainsVary"], validity, testRequirement)
    

#########################################################

def addAssertion(graph, testSubject, test, validity, testRequirement):
    assertion = BNode()
    resultSubject = BNode()
    
    # link the nodes
    graph.add((assertion, EARL["result"], resultSubject))
        
    graph.add((assertion, RDF["type"], EARL["Assertion"]))
    graph.add((assertion, EARL["assertedBy"], VAPOUR_SOFT["vapour2-0"]))
    graph.add((assertion, EARL["subject"], testSubject));
    graph.add((assertion, EARL["mode"], EARL["automatic"]))
    graph.add((assertion, EARL["test"], test))
    
    graph.add((resultSubject, RDF["type"], EARL["TestResult"]))
    if (validity == True):
        validityResource = EARL["passed"]
    else:
        validityResource = EARL["failed"]
    graph.add((resultSubject, EARL["validity"], validityResource))

    #graph.add((assertion, DCT["isPartOf"], testRequirement))
    graph.add((testRequirement, DCT["hasPart"], assertion))

def addTestRequirement(graph, title, order):
    global reqCount
    testRequirement = URIRef("req" + str(reqCount))
    reqCount += 1
    graph.add((testRequirement, RDF["type"], EARL["TestRequirement"]))
    graph.add((testRequirement, VAPOUR_VOCAB["order"], Literal(order)))
    titleLiteral = Literal(title)
    titleLiteral.language = "en"
    graph.add((testRequirement, DC["title"], titleLiteral))    
    return testRequirement

