from util import *
from vapour.namespaces import *
import httplib, urlparse
from rdflib import URIRef

# NOTE: The resolution of the httpRange-14 issue [1] covers just
# HTTP 'GET' requests. Nothing is said about 'HEAD' requests. However
# the HTTP specification [2] says that 'HEAD' requests are "identical to
# GET except that the server MUST NOT return a message-body in
# the response". Therefore, we assume that the conclusions of
# httpRange-14 still hold for 'HEAD' requests.
#
# [1] http://lists.w3.org/Archives/Public/www-tag/2005Jun/0039.html
# [2] http://www.w3.org/Protocols/rfc2616/rfc2616-sec9.html#sec9.4

def httpRange14Conclusions(graph, rootTestSubject):
    testSubjects = testSubjectsAsList(graph, rootTestSubject)
    for testSubject in testSubjects:
        requestUri = getRequestUri(graph, testSubject)
        parsedUri = urlparse.urlparse(requestUri) # (protocol,server,path,params,query,fragment)
        actuallyRequestedUri = urlparse.urlunparse((parsedUri[0], parsedUri[1], parsedUri[2], parsedUri[3], parsedUri[4], ""))
        if parsedUri[5] is not "":
            graph.add( (testSubject, VAPOUR["httpRange14ConclusionOn"], URIRef(requestUri) ) )
            graph.add( (URIRef(requestUri), RDF["type"], VAPOUR["AnyResource"] ) )
        statusCodeNumber = getResponseCode(graph, testSubject)
        graph.add((testSubject, VAPOUR["httpRange14ConclusionOn"], URIRef(actuallyRequestedUri)))
        if statusCodeNumber == httplib.OK:
            graph.add((URIRef(actuallyRequestedUri), RDF["type"], VAPOUR["InformationResource"]))
        elif statusCodeNumber == httplib.SEE_OTHER:
            graph.add((URIRef(actuallyRequestedUri), RDF["type"], VAPOUR["AnyResource"]))
