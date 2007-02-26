from vapour.namespaces import VAPOUR_VOCAB

def testSubjectsAsList(graph, rootTestSubject):
    list = [rootTestSubject]
    nextSubjects  = [x for x in graph.objects(rootTestSubject, VAPOUR_VOCAB["nextSubject"])]
    if (len(nextSubjects) == 1):
        list.extend(testSubjectsAsList(graph, nextSubjects[0]))
    return list

def lastTestSubjectOfSequence(graph, rootTestSubject):    
    return testSubjectsAsList(graph, rootTestSubject)[-1]