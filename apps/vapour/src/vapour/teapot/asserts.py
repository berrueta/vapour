
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
        addAssertion(graph, testSubject, RECIPES["TestResponseCode302"], result, testRequirement)

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

def assertLastResponseValidRdfData(graph, rootTestSubject, testRequirement):
    testSubject = lastTestSubjectOfSequence(graph, rootTestSubject)
    result = (mimetypes.rdfXml in getContentType(graph, testSubject))
    addAssertion(graph, testSubject, RECIPES["TestValidRdfData"], result, testRequirement)

def assertLastResponseContainsResourceDefinition(graph, rootTestSubject, testRequirement):
    testSubject = lastTestSubjectOfSequence(graph, rootTestSubject)
    result = (mimetypes.rdfXml in getContentType(graph, testSubject))
    addAssertion(graph, testSubject, RECIPES["TestContainsResourceDefinition"], result, testRequirement)

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
    
def addAssertion(graph, testSubject, test, validity, testRequirement):
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
    
    graph.add((assertion, DCT["isPartOf"], testRequirement))
    graph.add((testRequirement, DCT["hasPart"], assertion))
    
    return assertion

def addTestRequirement(graph, title):
    global reqCount
    testRequirement = URIRef("req" + str(reqCount))
    reqCount += 1
    graph.add((testRequirement, RDF["type"], EARL["TestRequirement"]))
    titleLiteral = Literal(title)
    titleLiteral.language = "en"
    graph.add((testRequirement, DC["title"], titleLiteral))    
    return testRequirement

