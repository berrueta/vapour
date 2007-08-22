import web
from vapour.strainer import strainer
from vapour.teapot import recipes, autodetect
from vapour.cup import common

class cup:
      def GET(self, format="html"):
            args = web.input()
            vocabUri = None #args["vocabUri"]
            classUri = None #args["classUri"]
            propUri = None #args["propUri"]
            
            store = common.createStore()
                
            if vocabUri is not None:
                if classUri is None and propertyUri is None:
                    (classUris, propertyUris) = autodetect.autodetectUris(store, vocabUri)    
                    random.seed()
                    if classUri is None and classUris is not None and len(classUris) > 0:
                        classUri = random.choice(classUris)
                    if propertyUri is None and propertyUris is not None and len(propertyUris) > 0:
                        propertyUri = random.choice(propertyUris)
                
                htmlVersions = True
                recipes.checkRecipes(store, htmlVersions, vocabUri, classUri, propUri)
                
                #if format is "html":        
                store.parse(common.pathToRdfFiles + "/vapour.rdf")
                store.parse(common.pathToRdfFiles + "/recipes.rdf")
                store.parse(common.pathToRdfFiles + "/earl.rdf")        
                model = common.createModel(store)
                web.header("Content-Type", "application/xhtml+xml", unique=True)
                web.output(strainer.resultsModelToHTML(model, vocabUri, classUri, propUri, common.pathToTemplates))
                #elif format is "rdf":
                #web.header("Content-Type", "application/rdf+xml", unique=True)
                #web.output(store.serialize(format="pretty-xml"))
            else:
                web.header("Content-Type", "application/xhtml+xml", unique=True)
                web.output(strainer.justTheFormInHTML(common.pathToTemplates))
          
urls = (
      '/(.*)', 'cup'
  )

web.webapi.internalerror = web.debugerror

if __name__ == "__main__":
    common.readEnvironment()
    web.run(urls, globals(), web.reloader)