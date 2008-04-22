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

def checkRecipes(graph, htmlVersions, vocabUri, classUri = None, propertyUri = None):
    checkWithoutAcceptHeader(graph, vocabUri, classUri, propertyUri)
    checkWithAcceptRdf(graph, vocabUri, classUri, propertyUri)
    if htmlVersions:
        #checkWithAcceptHtml(graph, vocabUri, classUri, propertyUri)
        #checkWithAcceptXhtml(graph, vocabUri, classUri, propertyUri)
        checkWithAcceptXhtmlOrHtml(graph, vocabUri, classUri, propertyUri)
    
    #for i in range(0,8):
     #   checkWithMixedAccept(graph, vocabUri, classUri, propertyUri, i)

def checkWithoutAcceptHeader(graph, vocabUri, classUri, propertyUri):
    scenarioDescription = " (without content negotiation)"
    contentType = None
    runScenario(graph, vocabUri, classUri, propertyUri, scenarioDescription, contentType)
    
def checkWithAcceptRdf(graph, vocabUri, classUri, propertyUri):
    scenarioDescription = " (requesting RDF/XML)"
    contentType = mimetypes.rdfXml
    runScenario(graph, vocabUri, classUri, propertyUri, scenarioDescription, contentType)
    
def checkWithAcceptHtml(graph, vocabUri, classUri, propertyUri):
    scenarioDescription = " (requesting HTML)"
    contentType = mimetypes.html
    runScenario(graph, vocabUri, classUri, propertyUri, scenarioDescription, contentType)
    
def checkWithAcceptXhtml(graph, vocabUri, classUri, propertyUri):
    scenarioDescription = " (requesting XHTML)"
    contentType = mimetypes.xhtml
    runScenario(graph, vocabUri, classUri, propertyUri, scenarioDescription, contentType)
    
def checkWithAcceptXhtmlOrHtml(graph, vocabUri, classUri, propertyUri):
    scenarioDescription = " (requesting (X)HTML)"
    contentType = mimetypes.xhtmlOrHtml
    runScenario(graph, vocabUri, classUri, propertyUri, scenarioDescription, contentType)
    
def checkWithMixedAccept(graph, vocabUri, classUri, propertyUri, mixNum):
    scenarioDescription = " (requesting a mix of MIME types: '" + mimetypes.mixed[mixNum] + "')"
    contentType = mimetypes.mixed[mixNum]
    runScenario(graph, vocabUri, classUri, propertyUri, scenarioDescription, contentType)    
    
def runScenario(graph, vocabUri, classUri, propertyUri, scenarioDescription, contentType):
    testRequirement = addTestRequirement(graph, "Dereferencing the vocabulary URI" + scenarioDescription)
    rootTestSubject = launchHttpDialog(graph, "dereferencing vocabulary URI", vocabUri, contentType, method = "HEAD")
    assertLastResponseCode200(graph, rootTestSubject, testRequirement)
    assertIntermediateResponseCode303(graph, rootTestSubject, testRequirement)
    assertLastResponseContentTypeFunctions[contentType](graph, rootTestSubject, testRequirement)

    if classUri is not None:
        testRequirement = addTestRequirement(graph, "Dereferencing class URI" + scenarioDescription)
        rootTestSubject = launchHttpDialog(graph, "dereferencing class URI", classUri, contentType, method = "HEAD")
        assertLastResponseCode200(graph, rootTestSubject, testRequirement)
        assertIntermediateResponseCode303(graph, rootTestSubject, testRequirement)
        assertLastResponseContentTypeFunctions[contentType](graph, rootTestSubject, testRequirement)
    
    if propertyUri is not None:
        testRequirement = addTestRequirement(graph, "Dereferencing property URI" + scenarioDescription)
        rootTestSubject = launchHttpDialog(graph, "dereferencing property URI", propertyUri, contentType, method = "HEAD")    
        assertLastResponseCode200(graph, rootTestSubject, testRequirement)
        assertIntermediateResponseCode303(graph, rootTestSubject, testRequirement)
        assertLastResponseContentTypeFunctions[contentType](graph, rootTestSubject, testRequirement)    

if __name__ == "__main__":
    store = Graph()
    example = "http://vapour.sourceforge.net/recipes-web/example1"
    recipe1(g, example, example, example)
    for s, p, o in store: 
        print s, p, o
    store.save('recipe1-test.rdf')

