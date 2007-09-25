
import sys
from vapour.strainer import strainer
from vapour.teapot import recipes, autodetect
from vapour.cup import common
import random

resourceBaseUri = "../resources"

if __name__ == "__main__":

    common.readEnvironment()
    
    vocabUri = sys.argv[1]
    classUri = sys.argv[2]
    propUri = sys.argv[3]
    outputFileName = sys.argv[4]
    outputRdfFileName = sys.argv[5]
    
    store = common.createStore()
        
    if classUri is None and propertyUri is None:
        (classUris, propertyUris) = autodetect.autodetectUris(store, vocabUri)    
        random.seed()
        if classUri is None and classUris is not None and len(classUris) > 0:
            classUri = random.choice(classUris)
        if propertyUri is None and propertyUris is not None and len(propertyUris) > 0:
            propertyUri = random.choice(propertyUris)
    
    htmlVersions = True
    recipes.checkRecipes(store, htmlVersions, vocabUri, classUri, propUri)
    if classUri is not None:
        namespaceFlavour = autodetect.autodetectNamespaceFlavour(vocabUri, classUri)
        validRecipes = autodetect.autodetectValidRecipes(vocabUri, classUri, namespaceFlavour, htmlVersions)
    else:
        namespaceFlavour = None
        validRecipes = []
    
    if outputRdfFileName is not None:
        outputRdfFile = open(outputRdfFileName,'w')
        outputRdfFile.write(store.serialize(format="pretty-xml"))
        outputRdfFile.close()

    store.parse(common.pathToRdfFiles + "/vapour.rdf")
    store.parse(common.pathToRdfFiles + "/recipes.rdf")
    store.parse(common.pathToRdfFiles + "/earl.rdf")

    model = common.createModel(store)
    html = strainer.resultsModelToHTML(model, vocabUri, classUri, propUri, 
                                       False, False, False, False,
                                       namespaceFlavour, validRecipes,
                                       resourceBaseUri, common.pathToTemplates)
    if outputFileName is not None:
        outputFile = open(outputFileName,'w')
        outputFile.write(str(html))
        outputFile.close()
    else:
        print html
        
