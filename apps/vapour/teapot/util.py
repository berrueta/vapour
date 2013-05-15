from vapour.namespaces import *

def testSubjectsAsList(graph, rootTestSubject):
    list = [rootTestSubject]
    nextSubjects  = [x for x in graph.objects(rootTestSubject, VAPOUR["nextSubject"])]
    if (len(nextSubjects) == 1):
        list.extend(testSubjectsAsList(graph, nextSubjects[0]))
    return list

def lastTestSubjectOfSequence(graph, rootTestSubject):    
    return testSubjectsAsList(graph, rootTestSubject)[-1]

###########################################################

def getRequestUri(graph, testSubject):
    httpRequest = getHttpRequest(graph, testSubject)
    return str(getLiteralProperty(graph, httpRequest, URI["uri"]))

def getResponseCode(graph, testSubject):
    httpResponse = getHttpResponse(graph, testSubject)
    return int(getLiteralProperty(graph, httpResponse, HTTP["statusCodeNumber"]))

def getContentType(graph, testSubject):
    httpResponse = getHttpResponse(graph, testSubject)
    return str(getLiteralProperty(graph, httpResponse, HTTP["content-type"]))

def getHttpRequest(graph, testSubject):
    l = [x for x in graph.subjects(HTTP["response"], testSubject)]
    return l[0]

def getHttpResponse(graph, testSubject):
    return testSubject # testSubject = response

def getLiteralProperty(graph, resource, property):
    l = [x for x in graph.objects(resource, property)]
    if len(l) == 0: return None
    else: return l[0]

###########################################################

import threading

class AtomicCounter:
    def __init__(self):
        self.value = 0L
        self.lock = threading.RLock()

    def getNext(self):
        self.lock.acquire()
        currentValue = self.value
        self.value += 1
        self.lock.release()
        return currentValue
