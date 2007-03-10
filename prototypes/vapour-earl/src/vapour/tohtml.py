from rdflib import Graph, Namespace
from rdflib.sparql import sparqlGraph
from rdflib.sparql.graphPattern import GraphPattern

EARL = Namespace("http://www.w3.org/WAI/ER/EARL/nmg-strawman#")
RDF = Namespace("http://www.w3.org/1999/02/22-rdf-syntax-ns#")
RDFS = Namespace("http://www.w3.org/2000/01/rdf-schema#")
DC = Namespace("http://purl.org/dc/elements/1.1/")
URI = Namespace("http://www.w3.org/2006/uri#")
HTTP = Namespace("http://www.w3.org/2006/http#")

store = Graph()

store.parse("../../../../webpage/vapour.rdf")
store.parse("../../../../webpage/recipes.rdf")
store.parse("../../../../webpage/earl.rdf")

store.parse("../../../../webpage/demo-report1.rdf")

sparqlGr = sparqlGraph.SPARQLGraph(store)

#for s, p, o in store: print s, p, o

print """
<html>
  <head>
    <title>Vapour Report</title>
  </head>
  <body>
    <h1>Vapour Report</h1>
"""

print "<h2>Test results</h2>"
select = ("?assertion", "?test", "?testTitle", "?validity", "?validityLabel")
where = GraphPattern([
                      ("?assertion", RDF["type"], EARL["Assertion"]),
                      ("?assertion", EARL["test"], "?test"),
                      ("?test", DC["title"], "?testTitle"),
                      ("?assertion", EARL["result"], "?result"),
                      ("?result", EARL["validity"], "?validity"),
                      ("?validity", RDFS["label"], "?validityLabel")
                     ])
print "<ul>"
for row in sparqlGr.query(select, where):
    print "<li>", row[2], ":", row[4], "</li>"
print "</ul>"

print "<h2>HTTP trace</h2>"
select = ("?testSub", "?testSubTitle", "?uri", "?responseCode", "?responseContentType")
where = GraphPattern([
                      ("?testSub", RDF["type"], EARL["TestSubject"]),
                      ("?testSub", DC["title"], "?testSubTitle"),
                      ("?testSub", EARL["httpRequest"], "?request"),
                      ("?request", URI["uri"], "?uri"),
                      ("?testSub", EARL["httpResponse"], "?response"),
                      ("?response", HTTP["responseCode"], "?responseCode"),
                      ("?response", HTTP["content-type"], "?responseContentType")
                      ])
print "<ul>"
for row in sparqlGr.query(select, where):
    print "<li>", row[1], ":", row[2], "(", row[3], ",", row[4], ")",  "</li>"
print "<ul>"

print """
  </body>
</html>
"""
