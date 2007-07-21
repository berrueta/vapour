
import os, sys
from rdflib.Graph import ConjunctiveGraph, Graph
from rdflib.sparql import sparqlGraph
from vapour.strainer import strainer
from vapour.teapot import recipes, autodetect
from vapour.namespaces import *
import random

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
    outputFileName = sys.argv[5]
    outputRdfFileName = sys.argv[6]
    
    store = Graph()
    store.bind('earl', EARL)
    store.bind('rdf', RDF)
    store.bind('rdfs', RDFS)
    store.bind('dc', DC)
    store.bind('dct', DCT)
    store.bind('uri', URI)
    store.bind('http', HTTP)
    store.bind('vapourv', VAPOUR_VOCAB)
    store.bind('vapour', VAPOUR_SOFT)
    store.bind('recipes', RECIPES)
    store.bind('foaf', FOAF)
    
    
    recipesFunctions = { 1 : recipes.recipe1,
                         2 : recipes.recipe2,
                         3 : recipes.recipe3,
                         4 : recipes.recipe4,
                         5 : recipes.recipe5
                       }
    
    if classUri is None and propertyUri is None:
        (classUris, propertyUris) = autodetect.autodetectUris(store, vocabUri)    
        random.seed()
        if classUri is None and classUris is not None and len(classUris) > 0:
            classUri = random.choice(classUris)
        if propertyUri is None and propertyUris is not None and len(propertyUris) > 0:
            propertyUri = random.choice(propertyUris)
    
    if recipeNumber in recipesFunctions:
        recipe = recipesFunctions[recipeNumber]
        recipe(store, vocabUri, classUri, propUri)
    else:
        print "ERROR: Unknown recipe number: " + recipeNumber
        sys.exit(-1)
    
    if outputRdfFileName is not None:
        outputRdfFile = open(outputRdfFileName,'w')
        outputRdfFile.write(store.serialize(format="pretty-xml"))
        outputRdfFile.close()

    store.parse(pathToRdfFiles + "/vapour.rdf")
    store.parse(pathToRdfFiles + "/recipes.rdf")
    store.parse(pathToRdfFiles + "/earl.rdf")

    model = sparqlGraph.SPARQLGraph(store)
    html = strainer.resultsModelToHTML(model, pathToTemplates)
    if outputFileName is not None:
        outputFile = open(outputFileName,'w')
        outputFile.write(str(html))
        outputFile.close()
    else:
        print html
        
