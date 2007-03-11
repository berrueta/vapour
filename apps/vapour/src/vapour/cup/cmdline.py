from rdflib.Graph import ConjunctiveGraph, Graph
from rdflib.sparql import sparqlGraph
import os, sys
from vapour.strainer import strainer
from vapour.teapot import recipes

if os.environ.get("VAPOUR_RDF_FILES"):
    pathToRdfFiles = os.environ.get("VAPOUR_RDF_FILES")
else:
    pathToRdfFiles = "http://vapour.sourceforge.net"
    
if os.environ.get("VAPOUR_TEMPLATES"):
    pathToTemplates = os.environ.get("VAPOUR_TEMPLATES")
else:
    pathToTemplates = "../strainer/templates"

if __name__ == "__main__":

    recipeNumber = int(sys.argv[1])
    vocabUri = sys.argv[2]
    classUri = sys.argv[3]
    propUri = sys.argv[4]
    
    store = Graph()
    store.parse(pathToRdfFiles + "/vapour.rdf")
    store.parse(pathToRdfFiles + "/recipes.rdf")
    store.parse(pathToRdfFiles + "/earl.rdf")
    
    if recipeNumber == 1:
        recipes.recipe1(store, vocabUri, classUri, propUri)
    else:
        print "ERROR: Unknown recipe number: " + recipeNumber
        sys.exit(-1)
    
    model = sparqlGraph.SPARQLGraph(store)
    t = strainer.resultsModelToHTML(model, pathToTemplates)
    print t
