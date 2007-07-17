
from rdflib import Graph
from httpdialog import launchHttpDialog
from asserts import *
import mimetypes

assertLastResponseContentTypeFunctions = {
                                          mimetypes.rdfXml : assertLastResponseContentTypeRdf,
                                          mimetypes.html : assertLastResponseContentTypeHtml,
                                          mimetypes.qualifiedRdfXml :  assertLastResponseContentTypeRdf,
                                          mimetypes.qualifiedHtml : assertLastResponseContentTypeHtml,
                                          None : assertLastResponseContentTypeRdf
                                }    

# it needs a refactor into OOP

def recipe1(graph, vocabUri, classUri, instanceUri):
    checkWithoutAcceptHeader(graph, vocabUri, classUri, instanceUri)

def recipe2(graph, vocabUri, classUri, instanceUri):
    checkWithoutAcceptHeader(graph, vocabUri, classUri, instanceUri);

def recipe3(graph, vocabUri, classUri, instanceUri):
    checkWithoutAcceptHeader(graph, vocabUri, classUri, instanceUri)
    checkWithAcceptRdf(graph, vocabUri, classUri, instanceUri)
    checkWithAcceptHtml(graph, vocabUri, classUri, instanceUri)
    checkWithAcceptRdfQualified(graph, vocabUri, classUri, instanceUri)
    checkWithAcceptHtmlQualified(graph, vocabUri, classUri, instanceUri)
    
def recipe4(graph, vocabUri, classUri, instanceUri):
     #FIXME
    checkWithoutAcceptHeader(graph, vocabUri, classUri, instanceUri)
    checkWithAcceptRdf(graph, vocabUri, classUri, instanceUri)
    checkWithAcceptHtml(graph, vocabUri, classUri, instanceUri)
    checkWithAcceptRdfQualified(graph, vocabUri, classUri, instanceUri)
    checkWithAcceptHtmlQualified(graph, vocabUri, classUri, instanceUri)
    
def recipe5(graph, vocabUri, classUri, instanceUri):
     #FIXME
    checkWithoutAcceptHeader(graph, vocabUri, classUri, instanceUri)
    checkWithAcceptRdf(graph, vocabUri, classUri, instanceUri)
    checkWithAcceptHtml(graph, vocabUri, classUri, instanceUri)
    checkWithAcceptRdfQualified(graph, vocabUri, classUri, instanceUri)
    checkWithAcceptHtmlQualified(graph, vocabUri, classUri, instanceUri)
    
def checkWithoutAcceptHeader(graph, vocabUri, classUri, instanceUri):
    scenarioDescription = " (without content negotiation)"
    contentType = None
    runScenario(graph, vocabUri, classUri, instanceUri, scenarioDescription, contentType)
    
def checkWithAcceptRdf(graph, vocabUri, classUri, instanceUri):
    scenarioDescription = " (requesting RDF/XML)"
    contentType = mimetypes.rdfXml
    runScenario(graph, vocabUri, classUri, instanceUri, scenarioDescription, contentType)
    
def checkWithAcceptHtml(graph, vocabUri, classUri, instanceUri):
    scenarioDescription = " (requesting HTML)"
    contentType = mimetypes.html
    runScenario(graph, vocabUri, classUri, instanceUri, scenarioDescription, contentType)
    
def checkWithAcceptRdfQualified(graph, vocabUri, classUri, instanceUri):
    scenarioDescription = " (requesting RDF/XML with qualifier)"
    contentType = mimetypes.qualifiedRdfXml
    runScenario(graph, vocabUri, classUri, instanceUri, scenarioDescription, contentType)

def checkWithAcceptHtmlQualified(graph, vocabUri, classUri, instanceUri):
    scenarioDescription = " (requesting HTML with qualifier)"
    contentType = mimetypes.qualifiedHtml
    runScenario(graph, vocabUri, classUri, instanceUri, scenarioDescription, contentType)
    
def runScenario(graph, vocabUri, classUri, instanceUri, scenarioDescription, contentType):
    testRequirement = addTestRequirement(graph, "Dereferencing the vocabulary URI" + scenarioDescription)
    rootTestSubject = launchHttpDialog(graph, "dereferencing vocabulary URI", vocabUri, contentType)
    assertLastResponseCode200(graph, rootTestSubject, testRequirement)
    assertIntermediateResponseCode303(graph, rootTestSubject, testRequirement)
    assertLastResponseContentTypeFunctions[contentType](graph, rootTestSubject, testRequirement)

    testRequirement = addTestRequirement(graph, "Dereferencing class URI" + scenarioDescription)
    rootTestSubject = launchHttpDialog(graph, "dereferencing class URI", classUri, contentType)
    assertLastResponseCode200(graph, rootTestSubject, testRequirement)
    assertIntermediateResponseCode303(graph, rootTestSubject, testRequirement)
    assertLastResponseContentTypeFunctions[contentType](graph, rootTestSubject, testRequirement)

    testRequirement = addTestRequirement(graph, "Dereferencing property URI" + scenarioDescription)
    rootTestSubject = launchHttpDialog(graph, "dereferencing property URI", instanceUri, contentType)    
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
