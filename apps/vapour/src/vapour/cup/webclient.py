#!/usr/bin/env python2.4

#path to work inside apache (uncomment these lines)
#import sys
#sys.path.append('../..')

import web
import random, traceback
from vapour.strainer import strainer
from vapour.teapot import recipes, validation, autodetect
from vapour.cup import common

resourceBaseUri = "http://vapour.sf.net/resources"

class cup:
      def GET(self, getArgs):
            web.header("Content-Type", "text/html; charset=utf-8") #IE sucks
            args = web.input()
            try:
                vocabUri = args["vocabUri"]
                if vocabUri is "": vocabUri = None
            except KeyError:
                vocabUri = None
            try:
                classUri = args["classUri"]
                if classUri is "": classUri = None
            except KeyError:
                classUri = None                
            try:
                propertyUri = args["propertyUri"]
                if propertyUri is "": propertyUri = None
            except KeyError:
                propertyUri = None

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
                autodetectClassUriIfEmpty = args["autodetectClassUri"] is "1"
            except KeyError:
                autodetectClassUriIfEmpty = False

            try:
                autodetectPropertyUriIfEmpty = args["autodetectPropertyUri"] is "1"
            except KeyError:
                autodetectPropertyUriIfEmpty = False

            try:
                store = common.createStore()
                    
                if vocabUri is not None:
                    logger.info("request over vocabulary on " + vocabUri)
                    if (classUri is None and autodetectClassUriIfEmpty) or (propertyUri is None and autodetectPropertyUriIfEmpty):
                        (classUris, propertyUris) = autodetect.autodetectUris(store, vocabUri)    
                        random.seed()
                        if autodetectClassUriIfEmpty and classUri is None and classUris is not None and len(classUris) > 0:
                            classUri = random.choice(classUris)
                        if autodetectPropertyUriIfEmpty and propertyUri is None and propertyUris is not None and len(propertyUris) > 0:
                            propertyUri = random.choice(propertyUris)
                    
                    recipes.checkRecipes(store, htmlVersions, vocabUri, classUri, propertyUri)
                    if validateRDF:
                        validation.validateRDF(store, vocabUri, classUri, propertyUri)
                    if classUri is not None:
                        namespaceFlavour = autodetect.autodetectNamespaceFlavour(vocabUri, classUri)
                        validRecipes = autodetect.autodetectValidRecipes(vocabUri, classUri, namespaceFlavour, htmlVersions)
                    else:
                        namespaceFlavour = None
                        validRecipes = []
                    
                    if format == "html":        
                        store.parse(common.pathToRdfFiles + "/vapour.rdf")
                        store.parse(common.pathToRdfFiles + "/recipes.rdf")
                        store.parse(common.pathToRdfFiles + "/earl.rdf")        
                        model = common.createModel(store)
                        web.header("Content-Type", "application/xhtml+xml", unique=True)
                        web.output(strainer.resultsModelToHTML(model, vocabUri, classUri, propertyUri, True,
                                                               autodetectClassUriIfEmpty, autodetectPropertyUriIfEmpty, 
                                                               validateRDF, htmlVersions, namespaceFlavour, 
                                                               validRecipes, resourceBaseUri, common.pathToTemplates))
                    elif format == "rdf":
                        web.header("Content-Type", "application/rdf+xml", unique=True)
                        web.output(store.serialize(format="pretty-xml"))
                    else:
                        web.ctx.status = "400 Bad Request"
                        web.output("<p>Unknown format " + format + "</p>")
                else:  # vocabUri is None
                    web.header("Content-Type", "application/xhtml+xml", unique=True)
                    web.output(strainer.justTheFormInHTML(resourceBaseUri, common.pathToTemplates))
            except Exception, e:
                logger.error(str(e))
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

