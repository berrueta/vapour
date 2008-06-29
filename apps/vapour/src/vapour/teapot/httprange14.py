from util import *
from vapour.namespaces import *
import httplib
from rdflib import URIRef

# NOTE: The resolution of the httpRange-14 issue [1] covers just
# HTTP 'GET' requests. Nothing is said about 'HEAD' requests. However
# the HTTP specification says that 'HEAD' requests are "identical to
# GET except that the server MUST NOT return a message-body in
#Êthe response". Therefore, we assume that the conclusions of
# httpRange-14 still hold for 'HEAD' requests.
#
#Ê[1] http://lists.w3.org/Archives/Public/www-tag/2005Jun/0039.html

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
