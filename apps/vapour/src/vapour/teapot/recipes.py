from rdflib import Graph
from httpdialog import followRedirects
from asserts import *
from validation import assertLastResponseBodyContainsDefinitionForResource
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
            #checkWithAcceptHtml(graph, vocabUri, classUri, propertyUri)
            #checkWithAcceptXhtml(graph, vocabUri, classUri, propertyUri)
            checkWithAcceptXhtmlOrHtml(graph, resource, validatorOptions)
    
        #for i in range(0,8):
         #   checkWithMixedAccept(graph, vocabUri, classUri, propertyUri, i)

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
    (rootTestSubject, httpResponse) = followRedirects(graph, "dereferencing " + resource['description'], resource['uri'], requestedContentType, httpMethod)
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
    return httpResponse

if __name__ == "__main__":
    store = Graph()
    example = "http://vapour.sourceforge.net/recipes-web/example1"
    checkRecipes(g, [{'uri': example, 'description': "Demo URI", 'priority': 1}], options.ValidatorOptions())
    for s, p, o in store: 
        print s, p, o
    store.save('recipe1-test.rdf')

