from vapour.namespaces import *
from vapour.common.vapourexceptions import *
from labeler import labelTestSubjects
from rdflib import Graph, BNode, Literal
import httplib
import urlparse
import datetime
import dns.resolver
from common import allowIntranet # FIXME: horrible hack, global variable!

maxRedirects = 3
defaultUserAgent = "vapour.sourceforge.net"

###########################################################

def followRedirects(graph, what, url, accept = None, method = "GET", userAgent = defaultUserAgent):
    '''Executes a multi-stage HTTP dialog following the redirects.
    
    Returns an array with two elements: firstly, the first
    test subject resource; secondly, the HTTP response object.'''
    redirectsCount = 0
    r = simpleRequest(graph, url, accept, redirectsCount, None, method, userAgent)
    firstTestSubjectResource = r[0]

    response = r[1]
    while (response.status == httplib.SEE_OTHER or
               response.status == httplib.FOUND or
               response.status == httplib.TEMPORARY_REDIRECT or
               response.status == httplib.MOVED_PERMANENTLY):
        previousSubjectResource = r[0]        
        url = response.getheader("Location")
        if (urlparse.urlparse(url)[0] != "http"):
            raise IlegalLocationValue(url)
        redirectsCount = redirectsCount + 1
        if (redirectsCount > maxRedirects):
            raise TooManyRedirections

        r = simpleRequest(graph, url, accept, redirectsCount, previousSubjectResource, method, userAgent)
        response = r[1]
        
    labelTestSubjects(graph, firstTestSubjectResource, what)                
    return (firstTestSubjectResource, response)
    
###########################################################
        
def simpleRequest(graph, url, accept, previousRequestCount, previousTestSubjectResource, method, userAgent):    
    '''Executes a single HTTP request and receives a response.
    
    Returns a duple containing: firstly, the test subject resource
    (note that there is only one, because this function does not
     handle HTTP redirects); secondly, the HTTP response object.'''
    parsedUrl = urlparse.urlparse(url)   # (_,host,path,_,_,_)
    host = parsedUrl[1]
    path = parsedUrl[2]

    if allowIntranet is False:
        # FIXME: skip DNS resolution if the host is already an IP address
        ipList = dns.resolver.query(str(host).split(":")[0])
        for ip in ipList:
            if str(ip).startswith("192.") or str(ip) is "127.0.0.1":
                raise ForbiddenAddress(str(ip), url)
    
    conn = httplib.HTTPConnection(host)
    headers = {"User-Agent": userAgent}
    if (accept is not None):
        headers["Accept"] = accept
    dateRequest = datetime.datetime.now()
    conn.request(method, getPathParamsAndQuery(url), headers = headers)
    dateResponse = datetime.datetime.now()
    response = conn.getresponse()
    
    testSubjectResource = addToGraph(graph, url, accept, response, previousRequestCount, method, userAgent, host, path, dateRequest, dateResponse)
    
    # makes a cross-link between the previous subject resource
    # and the new one
    if (previousTestSubjectResource is not None):
        graph.add((previousTestSubjectResource, VAPOUR_VOCAB["nextSubject"], testSubjectResource))
        graph.add((testSubjectResource, VAPOUR_VOCAB["previousSubject"], previousTestSubjectResource))

    return (testSubjectResource, response)
    
###########################################################

def addToGraph(graph, url, accept, response, previousRequestCount, method, userAgent, host, path, dateRequest, dateResponse):
    '''Creates a new test subject resource and fills its properties.
    
    The new test subject resource is a blank node, and
    it is added to the graph. This function returns the new
    test subject resource.'''
    httpStatus  = response.status
    location    = response.getheader("Location")
    contentLocation = response.getheader("Content-Location")
    contentType = response.getheader("Content-Type")
    vary        = response.getheader("Vary")

    # creates the new resources
    testSubjectResource = BNode()
    requestResource     = BNode()
    responseResource    = BNode()
    
    # link the resources
    graph.add((testSubjectResource, EARL["httpRequest"], requestResource))
    graph.add((testSubjectResource, EARL["httpResponse"], responseResource))
    
    # properties of the testSubjectResource
    # Not sure about adding this triple, the response is a different
    # resource...
    # graph.add((testSubjectResource, RDF["type"], HTTP["HttpResponse"]))
    graph.add((testSubjectResource, RDF["type"], EARL["TestSubject"]))
    graph.add((testSubjectResource, DC["date"], Literal(datetime.datetime.now()))) # FIXME: use standard format
    graph.add((testSubjectResource, VAPOUR_VOCAB["previousRequestCount"], Literal(previousRequestCount)))
    
    # properties of the requestResource
    graph.add((requestResource, RDF["type"], HTTP["Request"]))
    graph.add((requestResource, HTTP["methodName"], method))
    graph.add((requestResource, HTTP["method"], HTTP_METHODS[method]))
    # FIXME: the next property may be deprecated
    graph.add((requestResource, URI["uri"], Literal(url))) # FIXME: beware of 2nd requests
    graph.add((requestResource, HTTP["absoluteURI"], Literal(url)))
    graph.add((requestResource, HTTP["abs_path"], Literal(getPathParamsAndQuery(url))))
    graph.add((requestResource, HTTP["host"], Literal(host)))
    if (accept is not None):
        graph.add((requestResource, HTTP["accept"], Literal(accept)))
    graph.add((requestResource, HTTP["user-agent"], Literal(userAgent)))
    graph.add((requestResource, HTTP["httpVersion"], Literal("1.1")))
    graph.add((requestResource, DC["date"], Literal(dateRequest))) # FIXME: use standard format
        
    # properties of the responseResource
    graph.add((responseResource, RDF["type"], HTTP["Response"]))
    graph.add((responseResource, DC["date"], Literal(dateResponse))) # FIXME: use standard format
    graph.add((responseResource, HTTP["statusCodeNumber"], Literal(httpStatus)))
    graph.add((responseResource, HTTP["statusCode"], HTTP_STATUS_CODES["statusCode%d" % httpStatus]))
    if (location is not None): 
        graph.add((responseResource, HTTP["location"], Literal(location)))
    if (contentType is not None):
        graph.add((responseResource, HTTP["content-type"], Literal(contentType)))
    if (contentLocation is not None):
        graph.add((responseResource, HTTP["content-location"], Literal(contentLocation)))
    if (vary is not None):
        graph.add((responseResource, HTTP["vary"], Literal(vary)))
    if (httpStatus >= 400):
        addFormattedBody(graph, responseResource, response)
    
    # links the requestResource to the responseResource
    graph.add((requestResource, HTTP["response"], responseResource))
    
    return testSubjectResource

def getPathParamsAndQuery(url):
    parsedUrl = urlparse.urlparse(url) # (protocol,server,path,params,query,fragment)
    newUrl = ("", "", parsedUrl[2], parsedUrl[3], parsedUrl[4], "")
    return urlparse.urlunparse(newUrl)

def addFormattedBody(graph, responseResource, response):
    object = None
    if response.getheader("Content-Type").startswith("text/plain"):
        object = Literal(str(response.read()))
    if object is not None:
        graph.add((responseResource, HTTP["body"], object))

###########################################################
# debug code
#

if __name__ == "__main__":
    g = Graph()
    (rootTestSubject, httpResponse) = followRedirects(g, "dereferencing vocabulary URI", "http://www.google.com")
    #print "Sequence of testSubjects: ", util.testSubjectsAsList(g, rootTestSubject)
    for s, p, o in g: print s, p, o
    g.save('prueba.rdf')

