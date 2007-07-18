
from rdflib.Graph import ConjunctiveGraph
from rdflib.sparql.sparqlGraph import SPARQLGraph
from rdflib.sparql.graphPattern import GraphPattern
from rdflib.sparql import Query
from vapour.namespaces import *
from Cheetah.Template import Template
import datetime

try:
    import Cheetah
except ImportError:
    print >> stderr, "This program REQUIRE cheetah. Please install the library"
    sys.exit(-1)

try:
    import rdflib
except ImportError:
    print >>stderr, "This program REQUIRE rdflib. Please install the library"
    sys.exit(-1)


def getTestRequirements(model):
    sparqlGr = SPARQLGraph(model)
    select = ("?testRequirement", # 0
              "?testRequirementTitle" # 1
              )
    where = GraphPattern([
         ("?testRequirement", RDF["type"], EARL["TestRequirement"]),
         ("?testRequirement", DC["title"], "?testRequirementTitle")
         ])
    resultSet = Query.query(sparqlGr, select, where)
    # manually sorting the results
    sortByTitleFunc = lambda x, y : cmp(x[1],y[1]) 
    resultSet.sort(sortByTitleFunc)
    return resultSet

def getResultsFromModel(model, testRequirementUri):
    sparqlGr = SPARQLGraph(model)
    select = ("?assertion", #0
              "?test", # 1
              "?testTitle", # 2
              "?validity", # 3
              "?validityLabel", # 4
              "?subject", # 5
              "?subjectTitle") # 6
    where = GraphPattern([          
        ("?assertion", RDF["type"], EARL["Assertion"]),
        (testRequirementUri, DCT["hasPart"], "?assertion"),
        ("?assertion", EARL["test"], "?test"),
        ("?test", DC["title"], "?testTitle"),
        ("?assertion", EARL["result"], "?result"),
        ("?result", EARL["validity"], "?validity"),
        ("?validity", RDFS["label"], "?validityLabel"),
        ("?assertion", EARL["subject"], "?subject"),
        ("?subject", DC["title"], "?subjectTitle")
        ])
    resultSet = Query.query(sparqlGr, select, where)
    return resultSet

def getHttpTracesFromModel(model, testRequirementUri):
    sparqlGr = SPARQLGraph(model)
    select = (
              "?testSub", # 0
              "?testSubTitle", # 1
              "?uri", # 2

              "?responseCode", # 3
              "?responseContentType", # 4
              "?responseLocation",  # 5

              "?responseCodeTest", # 6
              "?responseCodeValidity", # 7
              "?responseContentTypeTest", # 8
              "?responseContentTypeValidity", # 9
              
              "?requestAccept", # 10
              "?previousRequestCount", # 11
              )
    where = GraphPattern([Concept.
        (testRequirementUri, DCT["hasPart"], "?assertion"),
        ("?assertion", EARL["subject"], "?testSub"),
        ("?testSub", RDF["type"], EARL["TestSubject"]),
        ("?testSub", DC["title"], "?testSubTitle"),
        ("?testSub", EARL["httpRequest"], "?request"),
        ("?request", URI["uri"], "?uri"),
        ("?testSub", EARL["httpResponse"], "?response"),
        ("?response", HTTP["responseCode"], "?responseCode"),
        ("?testSub", VAPOUR_VOCAB["previousRequestCount"], "?previousRequestCount")
    ])
    optional = [
        GraphPattern([("?request", HTTP["accept"], "?requestAccept")]),
        GraphPattern([("?response", HTTP["content-type"], "?responseContentType")]),
        GraphPattern([("?response", HTTP["location"], "?responseLocation")]),
        GraphPattern([
                      ("?responseCodeAssertion", EARL["subject"], "?testSub"),
                      ("?responseCodeAssertion", EARL["test"], "?responseCodeTest"),
                      ("?responseCodeTest", VAPOUR_VOCAB["propertyUnderTest"], HTTP["responseCode"]),
                      ("?responseCodeAssertion", EARL["result"], "?responseCodeResult"),
                      ("?responseCodeResult", EARL["validity"], "?responseCodeValidity")
        ]),
        GraphPattern([
                      ("?responseContentTypeAssertion", EARL["subject"], "?testSub"),
                      ("?responseContentTypeAssertion", EARL["test"], "?responseContentTypeTest"),
                      ("?responseContentTypeTest", VAPOUR_VOCAB["propertyUnderTest"], HTTP["content-type"]),
                      ("?responseContentTypeAssertion", EARL["result"], "?responseContentTypeResult"),
                      ("?responseContentTypeResult", EARL["validity"], "?responseContentTypeValidity")
        ])
    ]
    results = [x for x in Query.query(sparqlGr, select, where, optional)]
    # manually sorting the results
    sortByPreviousRequestCount = lambda x, y : cmp(x[11],y[11]) 
    results.sort(sortByPreviousRequestCount)    
    return results

def getFinalUriFromModel(model, testRequirementUri):
    sparqlGr = SPARQLGraph(model)
    select = ("?finalUri", "?contentType")
    # FIXME: a FILTER clause should be added to check the responseCode == 200
    where = GraphPattern([
        (testRequirementUri, DCT["hasPart"], "?assertion"),
        ("?assertion", EARL["subject"], "?testSubject"),
        ("?testSubject", EARL["httpRequest"], "?getRequest"),
        ("?testSubject", EARL["httpResponse"], "?httpResponse"),
        ("?httpResponse", HTTP["content-type"], "?contentType"),
        ("?getRequest", URI["uri"], "?finalUri")
    ])
    return [x for x in Query.query(sparqlGr, select, where)]

def getTestAgent(model):
    """
    Determine the software agent that was used to execute the tests
    """
    sparqlGr = SPARQLGraph(model)
    select = ("?agent", # 0
              "?agentTitle", # 1
              "?agentVersion", # 2
              "?agentHomepage" # 3
              )
    where = GraphPattern([
       ("?x", EARL["assertedBy"], "?agent"),
       ("?agent", DC["title"], "?agentTitle"),
       ("?agent", DCT["hasVersion"], "?agentVersion"),
       ("?agent", FOAF["homepage"], "?agentHomepage")
    ])
    results = Query.query(sparqlGr, select, where)
    return [x for x in results][0]

def sortTrace(trace):    
    # FIXME
    return trace

def resultsModelToHTML(model, templateDir = "templates"):
    """
    Entry point: use a RDFmodel with results as input to populate a
    cheetah template
    """
    data = {}
    data['testResults'] = {}
    data['httpTraces'] = {}
    data['finalUris'] = {}
    data['testRequirements'] = getTestRequirements(model)
    for testRequirementUri in [x[0] for x in data['testRequirements']]:        
        data['testResults'][testRequirementUri] = getResultsFromModel(model, testRequirementUri)
        data['httpTraces'][testRequirementUri] = sortTrace(getHttpTracesFromModel(model, testRequirementUri))
        data['finalUris'][testRequirementUri] = getFinalUriFromModel(model, testRequirementUri)
    data['testAgent'] = getTestAgent(model)
    data['reportDate'] = str(datetime.datetime.now())
    t = Template(file=templateDir + "/results.tmpl", searchList=[data])
    return t

if __name__ == "__main__":
    #
    # Test with local files
    #
    from rdflib.Graph import ConjunctiveGraph, Graph
    from rdflib.sparql import sparqlGraph
    
    store = Graph()
    store.parse("../../../../../webpage/vapour.rdf")
    store.parse("../../../../../webpage/recipes.rdf")
    store.parse("../../../../../webpage/earl.rdf")
    store.parse("../../../../../webpage/demo-report5.rdf")
    model = sparqlGraph.SPARQLGraph(store)
    t = resultsModelToHTML(model)
    print t
