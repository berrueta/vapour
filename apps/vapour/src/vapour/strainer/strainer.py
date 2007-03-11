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


from rdflib.sparql.graphPattern import GraphPattern
from vapour.namespaces import *

def getTestRequirements(model):
    select = ("?testRequirement", # 0
              "?testRequirementTitle" # 1
              )
    where = GraphPattern([
         ("?testRequirement", RDF["type"], EARL["TestRequirement"]),
         ("?testRequirement", DC["title"], "?testRequirementTitle")
         ])
    resultSet = model.query(select, where)
    return resultSet

def getResultsFromModel(model, testRequirementUri):
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
    resultSet = model.query(select, where)
    return resultSet

def getHttpTracesFromModel(model, testRequirementUri):
    select = ("?testSub", # 0
              "?testSubTitle", # 1
              "?uri", # 2
              "?responseCode", # 3
              "?responseContentType", # 4
              "?responseLocation") # 5
    where = GraphPattern([
        ("?testSub", RDF["type"], EARL["TestSubject"]),
        (testRequirementUri, DCT["hasPart"], "?assertion"),
        ("?assertion", EARL["subject"], "?testSub"),
        ("?testSub", DC["title"], "?testSubTitle"),
        ("?testSub", EARL["httpRequest"], "?request"),
        ("?request", URI["uri"], "?uri"),
        ("?testSub", EARL["httpResponse"], "?response"),
        ("?response", HTTP["responseCode"], "?responseCode")
    ])
    optional = GraphPattern([
        ("?response", HTTP["content-type"], "?responseContentType"),
        ("?response", HTTP["location"], "?responseLocation")
    ])
    results = model.query(select, where, optional)
    return results

def getFinalUriFromModel(model, testRequirementUri):
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
    return [x for x in model.query(select, where)]

def getTestAgent(model):
    """
    Determine the software agent that was used to execute the tests
    """
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
    results = model.query(select, where)
    return [x for x in results][0]
    

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
        data['httpTraces'][testRequirementUri] = getHttpTracesFromModel(model, testRequirementUri)
        data['finalUris'][testRequirementUri] = getFinalUriFromModel(model, testRequirementUri)
    data['testAgent'] = getTestAgent(model)
    data['passTestUri'] = str(EARL["pass"])
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
