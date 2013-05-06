
import sys, os
sys.path.append(os.path.abspath("../.."))
from datetime import datetime
from vapour.settings import PATH_RDF_FILES, PATH_TEMPLATES
from vapour.strainer import strainer
from vapour.teapot import recipes, autodetect, options
from vapour.cup import common
import random

resourceBaseUri = "../resources"

if __name__ == "__main__":

    # common.readEnvironment()
    
    vocabUri = sys.argv[1]
    outputFileName = sys.argv[2]
    outputRdfFileName = sys.argv[3]
    
    store = common.createStore()
        
    resourceToCheck = {'uri': vocabUri, 'description': "resource URI", 'order': 1}
    
    # defines the options of the validator
    validatorOptions = options.ValidatorOptions()
    validatorOptions.htmlVersions = True
    validatorOptions.defaultResponse = "dontmind"
    
    startTime = datetime.now()
    recipes.checkRecipes(store, resourceToCheck, validatorOptions)
    namespaceFlavour = None
    validRecipes = []
    
    if outputRdfFileName is not None:
        outputRdfFile = open(outputRdfFileName,'w')
        outputRdfFile.write(store.serialize(format="pretty-xml"))
        outputRdfFile.close()

    store.parse(PATH_RDF_FILES + "/vapour.rdf")
    store.parse(PATH_RDF_FILES + "/recipes.rdf")
    store.parse(PATH_RDF_FILES + "/earl.rdf")
    store.parse(PATH_RDF_FILES + "/http.rdf")        
    store.parse(PATH_RDF_FILES + "/vocab.rdf")        
    responseTime = datetime.now() - startTime
    responseTimeSeconds = round(responseTime.total_seconds() * 1000) / 1000;

    model = common.createModel(store)
    html = strainer.resultsModelToHTML(model, vocabUri, False, validatorOptions,
                                       namespaceFlavour, validRecipes, responseTimeSeconds,
                                       resourceBaseUri, PATH_TEMPLATES)
    if outputFileName is not None:
        outputFile = open(outputFileName,'w')
        outputFile.write(str(html))
        outputFile.close()
    else:
        print html

