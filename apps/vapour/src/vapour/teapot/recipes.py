
from rdflib import Graph
from httpdialog import launchHttpDialog
from asserts import *

# it needs a refactor into OOP

def recipe1(graph, vocabUri, classUri, instanceUri):
    testRequirement = addTestRequirement(graph, "Dereferencing the vocabulary URI")
    rootTestSubject = launchHttpDialog(graph, "dereferencing vocabulary URI", vocabUri)
    assertLastResponseCode200(graph, rootTestSubject, testRequirement)
    assertIntermediateResponseCode303(graph, rootTestSubject, testRequirement)
    assertLastResponseContentTypeRdf(graph, rootTestSubject, testRequirement)

    testRequirement = addTestRequirement(graph, "Dereferencing class URI")
    rootTestSubject = launchHttpDialog(graph, "dereferencing class URI", classUri)
    assertLastResponseCode200(graph, rootTestSubject, testRequirement)
    assertIntermediateResponseCode303(graph, rootTestSubject, testRequirement)
    assertLastResponseContentTypeRdf(graph, rootTestSubject, testRequirement)

    testRequirement = addTestRequirement(graph, "Dereferencing property URI")
    rootTestSubject = launchHttpDialog(graph, "dereferencing property URI", instanceUri)    
    assertLastResponseCode200(graph, rootTestSubject, testRequirement)
    assertIntermediateResponseCode303(graph, rootTestSubject, testRequirement)
    assertLastResponseContentTypeRdf(graph, rootTestSubject, testRequirement)
    
def recipe2(graph, vocabUri, classUri, instanceUri):
    testRequirement = addTestRequirement(graph, "Dereferencing the vocabulary URI")
    rootTestSubject = launchHttpDialog(graph, "dereferencing vocabulary URI", vocabUri)
    assertLastResponseCode200(graph, rootTestSubject, testRequirement)
    assertIntermediateResponseCode303(graph, rootTestSubject, testRequirement)
    assertLastResponseContentTypeRdf(graph, rootTestSubject, testRequirement)

    testRequirement = addTestRequirement(graph, "Dereferencing class URI")
    rootTestSubject = launchHttpDialog(graph, "dereferencing class URI", classUri)
    assertLastResponseCode200(graph, rootTestSubject, testRequirement)
    assertIntermediateResponseCode303(graph, rootTestSubject, testRequirement)
    assertLastResponseContentTypeRdf(graph, rootTestSubject, testRequirement)

    testRequirement = addTestRequirement(graph, "Dereferencing property URI")
    rootTestSubject = launchHttpDialog(graph, "dereferencing property URI", instanceUri)    
    assertLastResponseCode200(graph, rootTestSubject, testRequirement)
    assertIntermediateResponseCode303(graph, rootTestSubject, testRequirement)
    assertLastResponseContentTypeRdf(graph, rootTestSubject, testRequirement)
    
if __name__ == "__main__":
    store = Graph()
    example = "http://vapour.sourceforge.net/recipes-web/example1"
    recipe1(g, example, example, example)
    for s, p, o in store: 
        print s, p, o
    store.save('recipe1-test.rdf')
