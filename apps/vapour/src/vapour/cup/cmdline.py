
import os, sys
from rdflib.Graph import ConjunctiveGraph, Graph
from rdflib.sparql import sparqlGraph
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
    
    print sys.argv
    
    store = Graph()
    store.parse(pathToRdfFiles + "/vapour.rdf")
    store.parse(pathToRdfFiles + "/recipes.rdf")
    store.parse(pathToRdfFiles + "/earl.rdf")
    
    recipesFunctions = { 1 : recipes.recipe1,
                         2 : recipes.recipe2
                       }
    
    if recipeNumber in recipesFunctions:
        recipe = recipesFunctions[recipeNumber]
        recipe(store, vocabUri, classUri, propUri)
    else:
        print "ERROR: Unknown recipe number: " + recipeNumber
        sys.exit(-1)
    
    model = sparqlGraph.SPARQLGraph(store)
    html = strainer.resultsModelToHTML(model, pathToTemplates)
    print html
