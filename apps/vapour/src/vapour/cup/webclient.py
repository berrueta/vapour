import web
import random, traceback
from vapour.strainer import strainer
from vapour.teapot import recipes, autodetect
from vapour.cup import common

resourceBaseUri = "http://vapour.sf.net/resources"

class cup:
      def GET(self, format="html"):
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
                format = "html"
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
                    if (classUri is None and autodetectClassUriIfEmpty) or (propertyUri is None and autodetectPropertyUriIfEmpty):
                        (classUris, propertyUris) = autodetect.autodetectUris(store, vocabUri)    
                        random.seed()
                        if autodetectClassUriIfEmpty and classUri is None and classUris is not None and len(classUris) > 0:
                            classUri = random.choice(classUris)
                        if autodetectPropertyUriIfEmpty and propertyUri is None and propertyUris is not None and len(propertyUris) > 0:
                            propertyUri = random.choice(propertyUris)
                    
                    recipes.checkRecipes(store, htmlVersions, vocabUri, classUri, propertyUri)
                    
                    if format is "html":        
                        store.parse(common.pathToRdfFiles + "/vapour.rdf")
                        store.parse(common.pathToRdfFiles + "/recipes.rdf")
                        store.parse(common.pathToRdfFiles + "/earl.rdf")        
                        model = common.createModel(store)
                        web.header("Content-Type", "application/xhtml+xml", unique=True)
                        web.output(strainer.resultsModelToHTML(model, vocabUri, classUri, propertyUri, True,
                                                               autodetectClassUriIfEmpty, autodetectPropertyUriIfEmpty, htmlVersions, resourceBaseUri, common.pathToTemplates))
                    elif format is "rdf":
                        web.header("Content-Type", "application/rdf+xml", unique=True)
                        web.output(store.serialize(format="pretty-xml"))
                else:
                    web.header("Content-Type", "application/xhtml+xml", unique=True)
                    web.output(strainer.justTheFormInHTML(resourceBaseUri, common.pathToTemplates))
            except Exception, e:
                web.internalerror()
                web.output("<p>Vapour was unable to complete the request due to the following exception:</p>")
                web.output("<pre>" + traceback.format_exc(e) + "</pre>")
          
urls = (
      '/(.*)', 'cup'
  )

web.webapi.internalerror = web.debugerror

if __name__ == "__main__":
    common.readEnvironment()
    web.run(urls, globals(), web.reloader)