from rdflib import Graph
from httpdialog import launchHttpDialog
from asserts import *
import mimetypes

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
                                          None : assertLastResponseContentTypeRdf
                                }    

# it needs a refactor into OOP

def checkRecipes(graph, htmlVersions, resourcesToCheck):
    for resource in resourcesToCheck:
        # FIXME
        checkWithoutAcceptHeader(graph, resource)
        checkWithAcceptRdf(graph, resource)
        if htmlVersions:
            #checkWithAcceptHtml(graph, vocabUri, classUri, propertyUri)
            #checkWithAcceptXhtml(graph, vocabUri, classUri, propertyUri)
            checkWithAcceptXhtmlOrHtml(graph, resource)
    
        #for i in range(0,8):
         #   checkWithMixedAccept(graph, vocabUri, classUri, propertyUri, i)

def checkWithoutAcceptHeader(graph, resource):
    scenarioDescription = " (without content negotiation)"
    contentType = None
    runScenario(graph, resource, scenarioDescription, contentType)
    
def checkWithAcceptRdf(graph, resource):
    scenarioDescription = " (requesting RDF/XML)"
    contentType = mimetypes.rdfXml
    runScenario(graph, resource, scenarioDescription, contentType)
    
def checkWithAcceptHtml(graph, resource):
    scenarioDescription = " (requesting HTML)"
    contentType = mimetypes.html
    runScenario(graph, resource, scenarioDescription, contentType)
    
def checkWithAcceptXhtml(graph, resource):
    scenarioDescription = " (requesting XHTML)"
    contentType = mimetypes.xhtml
    runScenario(graph, resource, scenarioDescription, contentType)
    
def checkWithAcceptXhtmlOrHtml(graph, resource):
    scenarioDescription = " (requesting (X)HTML)"
    contentType = mimetypes.xhtmlOrHtml
    runScenario(graph, resource, scenarioDescription, contentType)
    
def checkWithMixedAccept(graph, resource, mixNum):
    scenarioDescription = " (requesting a mix of MIME types: '" + mimetypes.mixed[mixNum] + "')"
    contentType = mimetypes.mixed[mixNum]
    runScenario(graph, resource, scenarioDescription, contentType)    
    
def runScenario(graph, resource, scenarioDescription, contentType):
    testRequirement = addTestRequirement(graph, "Dereferencing " + resource['description'] + scenarioDescription)
    rootTestSubject = launchHttpDialog(graph, "dereferencing " + resource['description'], resource['uri'], contentType, method = "HEAD")
    assertLastResponseCode200(graph, rootTestSubject, testRequirement)
    assertIntermediateResponseCode303(graph, rootTestSubject, testRequirement)
    assertLastResponseContentTypeFunctions[contentType](graph, rootTestSubject, testRequirement)

if __name__ == "__main__":
    store = Graph()
    example = "http://vapour.sourceforge.net/recipes-web/example1"
    checkRecipes(g, True, [{'uri': example, 'description': "Demo URI", 'priority': 1}])
    for s, p, o in store: 
        print s, p, o
    store.save('recipe1-test.rdf')

