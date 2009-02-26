from rdflib.sparql.bison import Parse
from vapour.namespaces import *
from rdflib.sparql import Query
from rdflib import Graph
from httpdialog import followRedirects
from asserts import *
from validation import assertLastResponseBodyContainsDefinitionForResource
from httprange14 import httpRange14Conclusions
from util import lastTestSubjectOfSequence
import mimetypes, options

assertLastResponseContentTypeFunctions = {
                                          mimetypes.rdfXml : assertLastResponseContentTypeRdf,
                                          mimetypes.html : assertLastResponseContentTypeHtml,
                                          mimetypes.xhtml : assertLastResponseContentTypeXhtml,
                                          mimetypes.xhtmlOrHtml : assertLastResponseContentTypeXhtmlOrHtml,
                                          mimetypes.mixed[0] : assertLastResponseContentTypeRdf,
                                          mimetypes.mixed[1]: assertLastResponseContentTypeHtml,
                                          mimetypes.mixed[2]: assertLastResponseContentTypeRdf,
                                          mimetypes.mixed[3]: assertLastResponseContentTypeRdf,
                                          mimetypes.mixed[4]: assertLastResponseContentTypeHtml,
                                          mimetypes.mixed[5] :  assertLastResponseContentTypeRdf,
                                          mimetypes.mixed[6] : assertLastResponseContentTypeHtml,
                                          mimetypes.mixed[7] : assertLastResponseContentTypeXhtml,
#                                          None : assertLastResponseContentTypeRdf
                                }    

# it needs a refactor into OOP

def checkRecipes(graph, resourcesToCheck, validatorOptions):
    for resource in resourcesToCheck:
        # FIXME
        checkWithoutAcceptHeader(graph, resource, validatorOptions)
        checkWithAcceptRdf(graph, resource, validatorOptions)
        if validatorOptions.htmlVersions:
            #checkWithAcceptHtml(graph, resource, classUri, propertyUri)
            #checkWithAcceptXhtml(graph, resource, classUri, propertyUri)
            checkWithAcceptXhtmlOrHtml(graph, resource, validatorOptions)
    
        #for i in range(0,8):
        #    checkWithMixedAccept(graph, resource, i, validatorOptions)
    if validatorOptions.htmlVersions:
        checkVary(graph, validatorOptions)

def checkWithoutAcceptHeader(graph, resource, validatorOptions):
    scenarioDescription = " (without content negotiation)"
    requestedContentType = None
    runScenario(graph, resource, scenarioDescription, requestedContentType, validatorOptions, "GET")
    
def checkWithAcceptRdf(graph, resource, validatorOptions):
    scenarioDescription = " (requesting RDF/XML)"
    requestedContentType = mimetypes.rdfXml
    if validatorOptions.validateRdf:
        httpMethod = "GET"
    else:
        httpMethod = "HEAD"
    httpResponse = runScenario(graph, resource, scenarioDescription, requestedContentType, validatorOptions, httpMethod)
    
def checkWithAcceptHtml(graph, resource, validatorOptions):
    scenarioDescription = " (requesting HTML)"
    requestedContentType = mimetypes.html
    runScenario(graph, resource, scenarioDescription, requestedContentType, validatorOptions, "GET")
    
def checkWithAcceptXhtml(graph, resource, validatorOptions):
    scenarioDescription = " (requesting XHTML)"
    requestedContentType = mimetypes.xhtml
    runScenario(graph, resource, scenarioDescription, requestedContentType, validatorOptions, "GET")
    
def checkWithAcceptXhtmlOrHtml(graph, resource, validatorOptions):
    scenarioDescription = " (requesting (X)HTML)"
    requestedContentType = mimetypes.xhtmlOrHtml
    runScenario(graph, resource, scenarioDescription, requestedContentType, validatorOptions, "GET")
    
def checkWithMixedAccept(graph, resource, mixNum, validatorOptions):
    scenarioDescription = " (requesting a mix of MIME types: '" + mimetypes.mixed[mixNum] + "')"
    requestedContentType = mimetypes.mixed[mixNum]
    runScenario(graph, resource, scenarioDescription, requestedContentType, validatorOptions, "GET")    

def runScenario(graph, resource, scenarioDescription, requestedContentType, validatorOptions, httpMethod):
    testRequirement = addTestRequirement(graph, "Dereferencing " + resource['description'] + scenarioDescription, resource['order'])
    (rootTestSubject, httpResponse) = followRedirects(graph, "dereferencing " + resource['description'], resource['uri'], requestedContentType, httpMethod, validatorOptions.userAgent)
    assertLastResponseCode200(graph, rootTestSubject, testRequirement)
    assertIntermediateResponseCode303(graph, rootTestSubject, testRequirement)
    if requestedContentType is None:
        if validatorOptions.defaultResponse == "rdfxml":
            assertLastResponseContentTypeRdf(graph, rootTestSubject, testRequirement)
        elif validatorOptions.defaultResponse == "html":
            assertLastResponseContentTypeXhtmlOrHtml(graph, rootTestSubject, testRequirement)
    else:
        assertLastResponseContentTypeFunctions[requestedContentType](graph, rootTestSubject, testRequirement)
    if validatorOptions.validateRdf and (mimetypes.rdfXml in getContentType(graph, lastTestSubjectOfSequence(graph, rootTestSubject))):
        assertLastResponseBodyContainsDefinitionForResource(graph, resource, httpResponse, rootTestSubject, testRequirement)
    httpRange14Conclusions(graph, rootTestSubject)
    return httpResponse

def checkVary(graph, validatorOptions):
    query = """
    SELECT DISTINCT ?testSubject1 ?testSubject2 ?vary1 ?vary2 ?testReq1 ?testReq2 
    WHERE {
      ?testReq1     dct:hasPart       ?assert1 .
      ?testReq2     dct:hasPart       ?assert2 .
      ?assert1      earl:subject      ?testSubject1 .
      ?assert2      earl:subject      ?testSubject2 .
      ?testSubject1 earl:httpRequest  ?request1 .
      ?testSubject2 earl:httpRequest  ?request2 .
      ?request1     http:response     ?response1 .
      ?request2     http:response     ?response2 .
      ?request1     uri:uri           ?uri1 .
      ?request2     uri:uri           ?uri2 .
      ?request1     http:accept       ?accept1 .
      ?request2     http:accept       ?accept2 .
      ?response1    rdf:type          http:Response .
      ?response2    rdf:type          http:Response .
      ?response1    http:content-type ?contentType1 .
      ?response2    http:content-type ?contentType2 .
      ?response1    http:responseCode ?responseCode1 .
      ?response2    http:responseCode ?responseCode2 .
      FILTER (?uri1 = ?uri2) .
      FILTER (regex(?contentType1, '^application/rdf')) .
      FILTER (regex(?contentType2, '^(text/html)|(application/xhtml)')) .
      FILTER (?responseCode1 = 200) .
      FILTER (?responseCode2 = 200) .
      OPTIONAL {
        ?response1 http:vary ?vary1 .
        ?response2 http:vary ?vary2 .
      } .
    }"""
    tuples = graph.query(Parse(query), initNs=bindings).serialize('python')
    for t in tuples:
        testResult = t[2] is not None and t[3] is not None and ("Accept" in t[2]) and ("Accept" in t[3])
        assertVaryHeader(graph, t[0], testResult, t[4])
        assertVaryHeader(graph, t[1], testResult, t[5])

if __name__ == "__main__":
    store = Graph()
    example = "http://vapour.sourceforge.net/recipes-web/example1"
    checkRecipes(g, [{'uri': example, 'description': "Demo URI", 'priority': 1}], options.ValidatorOptions())
    for s, p, o in store: 
        print s, p, o
    store.save('recipe1-test.rdf')

