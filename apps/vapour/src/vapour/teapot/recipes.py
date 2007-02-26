from rdflib import Graph
from httpdialog import launchHttpDialog
from asserts import *

def recipe1(graph, vocabUri, classUri, instanceUri):
    rootTestSubject = launchHttpDialog(graph, "dereferencing vocabulary URI", vocabUri)
    assertLastResponseCode200(graph, rootTestSubject)
    assertIntermediateResponseCode303(graph, rootTestSubject)
    assertLastResponseContentTypeRdf(graph, rootTestSubject)

    rootTestSubject = launchHttpDialog(graph, "dereferencing class URI", classUri)

    rootTestSubject = launchHttpDialog(graph, "dereferencing instance URI", instanceUri)    
    
if __name__ == "__main__":
    g = Graph()
    recipe1(g, "http://vapour.sourceforge.net/recipes-web/example1",
            "http://vapour.sourceforge.net/recipes-web/example1",
            "http://vapour.sourceforge.net/recipes-web/example1")
    for s, p, o in g: print s, p, o
    g.save('prueba.rdf')