from util import *
from vapour.namespaces import *
import httplib
from rdflib import URIRef

def httpRange14Conclusions(graph, rootTestSubject):
    testSubjects = testSubjectsAsList(graph, rootTestSubject)
    for testSubject in testSubjects:
        requestUri = getRequestUri(graph, testSubject)
        responseCode = getResponseCode(graph, testSubject)
        graph.add((testSubject, VAPOUR_VOCAB["httpRange14ConclusionOn"], URIRef(requestUri)))
        if responseCode == httplib.OK:
            graph.add((URIRef(requestUri), RDF["type"], VAPOUR_VOCAB["InformationResource"]))
        elif responseCode == httplib.SEE_OTHER:
            graph.add((URIRef(requestUri), RDF["type"], VAPOUR_VOCAB["AnyResource"]))
