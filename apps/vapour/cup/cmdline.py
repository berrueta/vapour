
import sys
sys.path.append(os.path.abspath("../.."))

from vapour.settings import PATH_RDF_FILES, PATH_TEMPLATES
from vapour.strainer import strainer
from vapour.teapot import recipes, autodetect, options
from vapour.cup import common
import random

resourceBaseUri = "../resources"

if __name__ == "__main__":

    common.readEnvironment()
    
    vocabUri = sys.argv[1]
    classUri = sys.argv[2]
    propertyUri = sys.argv[3]
    instanceUri = None # FIXME
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
    
    resourcesToCheck = []
    if classUri is None and propertyUri is None and instanceUri is None:
        resourcesToCheck.append({'uri': vocabUri, 'description': "resource URI", 'order': 1})
    else:
        resourcesToCheck.append({'uri': vocabUri, 'description': "vocabulary URI", 'order': 1})
        if classUri is not None:
            resourcesToCheck.append({'uri': classUri, 'description': "class URI", 'order': 2})
        if propertyUri is not None:
            resourcesToCheck.append({'uri': propertyUri, 'description': "property URI", 'order': 3})
        if instanceUri is not None:
            resourcesToCheck.append({'uri': instanceUri, 'description': "instance URI", 'order': 4})
    
    # defines the options of the validator
    validatorOptions = options.ValidatorOptions()
    validatorOptions.htmlVersions = True
    validatorOptions.defaultResponse = "dontmind"
    
    recipes.checkRecipes(store, resourcesToCheck, validatorOptions)
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

    store.parse(PATH_RDF_FILES + "/vapour.rdf")
    store.parse(PATH_RDF_FILES + "/recipes.rdf")
    store.parse(PATH_RDF_FILES + "/earl.rdf")
    store.parse(PATH_RDF_FILES + "/http.rdf")        
    store.parse(PATH_RDF_FILES + "/vocab.rdf")        

    model = common.createModel(store)
    html = strainer.resultsModelToHTML(model, vocabUri, classUri, propertyUri, instanceUri, 
                                       False, False, False, False, defaultResponse,
                                       namespaceFlavour, validRecipes,
                                       resourceBaseUri, PATH_TEMPLATES)
    if outputFileName is not None:
        outputFile = open(outputFileName,'w')
        outputFile.write(str(html))
        outputFile.close()
    else:
        print html

