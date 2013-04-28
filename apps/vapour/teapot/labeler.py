from vapour.namespaces import DC
from rdflib import Graph, Literal
import util

def labelTestSubjects(graph, rootTestSubject, what, accept = None):
    sequence = util.testSubjectsAsList(graph, rootTestSubject)
    for i in range(0, len(sequence)):
        title = inttoord(i+1) + " request while " + what
        if (accept is None):
            title = title + " without specifying the desired content type"
        else:
            title = title + " " + mimetypes.requestDescription[accept]
        titleLiteral = Literal(title, lang = "en")
        graph.add((sequence[i], DC["title"], titleLiteral))
        
def inttoord(i):
    """I copied this function from http://simonwillison.net/2003/Oct/8/externalMemory/,
    probably we should check if it is in the public domain"""
    ordinal = [ ('th', 'st', 'nd', 'rd', 'th', 'th', 'th', 'th', 'th', 'th'),
                ('th', 'th', 'th', 'th', 'th', 'th', 'th', 'th', 'th', 'th')]
    ones = i % 10
    tens = (i % 100) / 10
    return str(i) + ordinal[tens==1][ones]