from rdflib import Graph
from httpdialog import launchHttpDialog
from asserts import *

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
    
if __name__ == "__main__":
    g = Graph()
    recipe1(g, "http://vapour.sourceforge.net/recipes-web/example1",
            "http://vapour.sourceforge.net/recipes-web/example1",
            "http://vapour.sourceforge.net/recipes-web/example1")
    for s, p, o in g: print s, p, o
    g.save('prueba.rdf')