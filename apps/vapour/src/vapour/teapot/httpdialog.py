from vapour.namespaces import *
from labeler import labelTestSubjects
from rdflib import Graph, BNode, Literal
import httplib
import urlparse
import datetime

userAgentString = "vapour.sourceforge.net"

def launchHttpDialog(graph, what, url, accept = None):
    r = simpleRequest(graph, url, accept)
    firstTestSubjectResource = r[0]

    response = r[1]
    while (response.status == httplib.SEE_OTHER or response.status == httplib.FOUND):
        previousSubjectResource = r[0]
        r = simpleRequest(graph, url, accept, previousSubjectResource)
        response = r[1]
        url = response.getheader("Location")
        
    labelTestSubjects(graph, firstTestSubjectResource, what)        
        
    return firstTestSubjectResource
        
def simpleRequest(graph, url, accept, previousTestSubjectResource = None):
    parsedUrl = urlparse.urlparse(url)   # (_,server,path,_,_,_)
    server = parsedUrl[1]
    path = parsedUrl[2]
    conn = httplib.HTTPConnection(server)
    headers = {"User-agent": userAgentString}
    if (accept is not None):
        headers["Accept"] = accept
    conn.request("GET", path, headers = headers)
    response = conn.getresponse()
    
    testSubjectResource = addToGraph(graph, url, accept, response)
    if (previousTestSubjectResource is not None):
        graph.add((previousTestSubjectResource, VAPOUR_VOCAB["nextSubject"], testSubjectResource))
        graph.add((testSubjectResource, VAPOUR_VOCAB["previousSubject"], previousTestSubjectResource))

    return (testSubjectResource, response)
    
def addToGraph(graph, url, accept, response):
    httpStatus = response.status
    location = response.getheader("Location")
    contentType = response.getheader("Content-Type")

    testSubjectResource = BNode()
    requestResource = BNode()
    responseResource = BNode()
    
    # link the resources
    graph.add((testSubjectResource, EARL["httpRequest"], requestResource))
    graph.add((testSubjectResource, EARL["httpResponse"], responseResource))
    
    graph.add((testSubjectResource, RDF["type"], EARL["TestSubject"]))
    graph.add((testSubjectResource, DC["date"], Literal(datetime.datetime.now()))) # FIXME: use standard format
    
    graph.add((responseResource, RDF["type"], HTTP["GetRequest"]))
    graph.add((requestResource, URI["uri"], Literal(url))) # FIXME: beware of 2nd requests
    if (accept is not None):
        graph.add((requestResource, HTTP["accept"], Literal(accept)))
    graph.add((requestResource, HTTP["user-agent"], Literal(userAgentString)))

    graph.add((responseResource, RDF["type"], HTTP["Response"]))
    graph.add((responseResource, HTTP["responseCode"], Literal(httpStatus)))
    if (location is not None): 
        graph.add((responseResource, HTTP["location"], Literal(location)))
    if (contentType is not None):
        graph.add((responseResource, HTTP["content-type"], Literal(contentType)))
        
    return testSubjectResource

if __name__ == "__main__":
    g = Graph()
    rootTestSubject = launchHttpDialog(g, "dereferencing vocabulary URI", "http://www.google.com")
    #print "Sequence of testSubjects: ", util.testSubjectsAsList(g, rootTestSubject)
    for s, p, o in g: print s, p, o
    g.save('prueba.rdf')