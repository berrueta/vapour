from Cheetah.Template import Template

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
from rdflib import Namespace


EARL = Namespace("http://www.w3.org/WAI/ER/EARL/nmg-strawman#")
RDF = Namespace("http://www.w3.org/1999/02/22-rdf-syntax-ns#")
RDFS = Namespace("http://www.w3.org/2000/01/rdf-schema#")
DC = Namespace("http://purl.org/dc/elements/1.1/")
URI = Namespace("http://www.w3.org/2006/uri#")
HTTP = Namespace("http://www.w3.org/2006/http#")

def getResultsFromModel(model):
    select = ("?assertion", "?test", "?testTitle",
              "?validity", "?validityLabel")
    where = GraphPattern([
        ("?assertion", RDF["type"], EARL["Assertion"]),
        ("?assertion", EARL["test"], "?test"),
        ("?test", DC["title"], "?testTitle"),
        ("?assertion", EARL["result"], "?result"),
        ("?result", EARL["validity"], "?validity"),
        ("?validity", RDFS["label"], "?validityLabel")
        ])
    resultSet = model.query(select, where)
    results = []
    for r in resultSet:
        results.append((r[2], r[4]))
    return results

def getHttpTracesFromModel(model):
    select = ("?testSub", "?testSubTitle", "?uri",
              "?responseCode", "?responseContentType")
    where = GraphPattern([
        ("?testSub", RDF["type"], EARL["TestSubject"]),
        ("?testSub", DC["title"], "?testSubTitle"),
        ("?testSub", EARL["httpRequest"], "?request"),
        ("?request", URI["uri"], "?uri"),
        ("?testSub", EARL["httpResponse"], "?response"),
        ("?response", HTTP["responseCode"], "?responseCode"),
        ("?response", HTTP["content-type"], "?responseContentType")
    ])
    results = model.query(select, where)
    return results
	


def resultsModelToHTML(model):
    """
    Entry point: use a RDFmodel with results as input to populate a
    cheetah template
    """
    data = {}
    data['testResults'] = getResultsFromModel(model)
    data['httpTraces'] = getHttpTracesFromModel(model)
    t = Template(file="templates/results.tmpl", searchList=[data])
    return t
	
if __name__ == "__main__":
    #
    # Test with local files
    #
    from rdflib.Graph import ConjunctiveGraph
    from rdflib.sparql import sparqlGraph
    
    store = ConjunctiveGraph()
    store.parse("../../../../../webpage/vapour.rdf")
    store.parse("../../../../../webpage/recipes.rdf")
    store.parse("../../../../../webpage/earl.rdf")
    store.parse("../../../../../webpage/demo-report1.rdf")
    model = sparqlGraph.SPARQLGraph(store)
    t = resultsModelToHTML(model)
    print t
