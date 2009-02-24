#!/usr/bin/python

#patch to work inside apache (uncomment these lines)
#import sys
#sys.path.append('../..')

import web
import random, traceback
from vapour.strainer import strainer
from vapour.teapot import recipes, autodetect, options
from vapour.cup import common

resourceBaseUri = "http://vapour.sf.net/resources"

class cup:
      def GET(self, getArgs):
            args = web.input()
            try:
                vocabUri = args["vocabUri"]
                if (vocabUri == "" or vocabUri == "http://"): vocabUri = None
            except KeyError:
                vocabUri = None
            try:
                classUri = args["classUri"]
                if (classUri == "" or classUri == "http://"): classUri = None
            except KeyError:
                classUri = None                
            try:
                propertyUri = args["propertyUri"]
                if (propertyUri == "" or propertyUri == "http://"): propertyUri = None
            except KeyError:
                propertyUri = None
            try:
                instanceUri = args["instanceUri"]
                if (instanceUri == "" or instanceUri == "http://"): instanceUri = None
            except KeyError:
                instanceUri = None
            try:
                defaultResponse = args["defaultResponse"]
                if defaultResponse != "rdfxml" and defaultResponse != "html" and defaultResponse != "dontmind":
                    defaultResponse = "dontmind" # default value
            except KeyError:
                defaultResponse = "dontmind"
            try:
                userAgent = args["userAgent"]
                if userAgent == "":
                    userAgent = options.defaultUserAgent
            except KeyError:
                userAgent = options.defaultUserAgent

            try:
                format = args["format"]
            except KeyError:
                if ((vocabUri is not None) and (web.ctx.environ.has_key("HTTP_ACCEPT"))):
                    format = common.getBestFormat(web.ctx.environ["HTTP_ACCEPT"])
                    logger.info("Using content negotiation to return report in %s" % format.upper())
                else:
                    format = "html"

            try:
                validateRDF = args["validateRDF"] is "1"
            except KeyError:
                validateRDF = False

            try:
                htmlVersions = args["htmlVersions"] is "1"
            except KeyError:
                htmlVersions = False

            try:
                autodetectUrisIfEmpty = args["autodetectUris"] is "1"
            except KeyError:
                autodetectUrisIfEmpty = False

            try:
                store = common.createStore()
                    
                if vocabUri is not None:
                    logger.info("request over vocabulary on " + vocabUri)
                    if (classUri is None and autodetectUrisIfEmpty) or (propertyUri is None and autodetectUrisIfEmpty):
                        (classUris, propertyUris, instanceUris) = autodetect.autodetectUris(store, vocabUri, userAgent)    
                        random.seed()
                        if autodetectUrisIfEmpty and classUri is None and classUris is not None and len(classUris) > 0:
                            classUri = random.choice(classUris)
                        if autodetectUrisIfEmpty and propertyUri is None and propertyUris is not None and len(propertyUris) > 0:
                            propertyUri = random.choice(propertyUris)
                        if autodetectUrisIfEmpty and instanceUri is None and instanceUris is not None and len(instanceUris) > 0:
                            instanceUri = random.choice(instanceUris)

                    # defines the resources to be checked  
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
                    validatorOptions = options.ValidatorOptions(htmlVersions, defaultResponse, validateRDF, userAgent)
                    
                    recipes.checkRecipes(store, resourcesToCheck, validatorOptions)
                    if classUri is not None:
                        namespaceFlavour = autodetect.autodetectNamespaceFlavour(vocabUri, classUri)
                        validRecipes = autodetect.autodetectValidRecipes(vocabUri, classUri, namespaceFlavour, htmlVersions)
                    else:
                        namespaceFlavour = None
                        validRecipes = []
                    
                    web.header("Vary", "Accept")
                    if format == "html":        
                        store.parse(common.pathToRdfFiles + "/vapour.rdf")
                        store.parse(common.pathToRdfFiles + "/recipes.rdf")
                        store.parse(common.pathToRdfFiles + "/earl.rdf")        
                        store.parse(common.pathToRdfFiles + "/http.rdf")        
                        store.parse(common.pathToRdfFiles + "/vocab.rdf")        
                        model = common.createModel(store)
                        web.header("Content-Type", "text/html; charset=utf-8") #IE sucks
                        web.output(strainer.resultsModelToHTML(model, vocabUri, classUri, propertyUri, instanceUri, True,
                                                               autodetectUrisIfEmpty, 
                                                               validatorOptions, namespaceFlavour, 
                                                               validRecipes, resourceBaseUri, common.pathToTemplates))
                    elif format == "rdf":
                        web.header("Content-Type", "application/rdf+xml; charset=utf-8")
                        web.output(store.serialize(format="pretty-xml"))
                    else:
                        web.header("Content-Type", "text/html; charset=utf-8") #IE sucks
                        web.ctx.status = "400 Bad Request"
                        web.output("<p>Unknown format " + format + "</p>")
                else:  # vocabUri is None
                    web.header("Content-Type", "text/html; charset=utf-8") #IE sucks
                    web.output(strainer.justTheFormInHTML(resourceBaseUri, common.pathToTemplates))
            except Exception, e:
                logger.error(str(e))
                web.header("Content-Type", "text/html; charset=utf-8") #IE sucks
                #web.internalerror()
                web.output(strainer.exceptionInHTML(e, resourceBaseUri, common.pathToTemplates))

          
urls = (
      '(.*)', 'cup'
  )

web.webapi.internalerror = web.debugerror

common.readEnvironment()

logger = common.createLogger()
application = web.wsgifunc(web.webpyfunc(urls, globals())) #seeAlso: http://webpy.org/install

if __name__ == "__main__":
    web.run(urls, globals(), web.reloader)

