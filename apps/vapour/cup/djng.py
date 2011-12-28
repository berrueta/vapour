
import random
import traceback
from django.http import HttpResponse, HttpResponseBadRequest
from vapour.strainer import strainer
from vapour.teapot import recipes, autodetect, options
from vapour.cup import common
from vapour.settings import DEBUG, MEDIA_URL, PATH_TEMPLATES, PATH_RDF_FILES, PATH_RESOURCES_FILES
from vapour.common.lang import if_else

resourceBaseUri = None
if DEBUG:
    resourceBaseUri = if_else(MEDIA_URL[-1] == "/", MEDIA_URL[:-1], MEDIA_URL) #remove last slash
else:
    resourceBaseUri = PATH_RESOURCES_FILES

class cup:

    @staticmethod
    def GET(request):
        
        logger = common.createLogger()

        try:
            vocabUri = request.GET.get("vocabUri")
            if (vocabUri == "" or vocabUri == "http://"): vocabUri = None
        except KeyError:
            vocabUri = None
        try:
            classUri = request.GET.get("classUri")
            if (classUri == "" or classUri == "http://"): classUri = None
        except KeyError:
            classUri = None                
        try:
            propertyUri = request.GET.get("propertyUri")
            if (propertyUri == "" or propertyUri == "http://"): propertyUri = None
        except KeyError:
            propertyUri = None
        try:
            instanceUri = request.GET.get("instanceUri")
            if (instanceUri == "" or instanceUri == "http://"): instanceUri = None
        except KeyError:
            instanceUri = None
        try:
            defaultResponse = request.GET.get("defaultResponse")
            if defaultResponse != "rdfxml" and defaultResponse != "html" and defaultResponse != "dontmind":
                defaultResponse = "dontmind" # default value
        except KeyError:
            defaultResponse = "dontmind"
        try:
            userAgent = request.META["HTTP_USER_AGENT"]
            if not userAgent:
                userAgent = options.defaultUserAgent
            elif "\n" in userAgent:
                userAgent = options.defaultUserAgent # prevent HTTP header injection
        except KeyError:
            userAgent = options.defaultUserAgent

        try:
            format = request.GET.get("format")
        except KeyError:
            if ((vocabUri is not None) and (request.META.has_key("HTTP_ACCEPT"))):
                format = common.getBestFormat(request.META["HTTP_ACCEPT"])
                logger.info("Using content negotiation to return report in %s" % format.upper())
        if format == None:
            format = "html"

        try:
            client = request.META.get('REMOTE_ADDR')
        except KeyError:
            client = None

        try:
            validateRDF = request.GET.get("validateRDF") is "1"
        except KeyError:
            validateRDF = False

        try:
            htmlVersions = request.GET.get("htmlVersions") is "1"
        except KeyError:
            htmlVersions = False

        try:
            autodetectUrisIfEmpty = request.GET.get("autodetectUris") is "1"
        except KeyError:
            autodetectUrisIfEmpty = False

        try:
            store = common.createStore()
                
            if vocabUri is not None:
                if (client):
                    logger.info("Request from %s over URI: %s" % (client, vocabUri))
                else:
                    logger.info("Request over URI: " + vocabUri)
                if (classUri is None and autodetectUrisIfEmpty) or (propertyUri is None and autodetectUrisIfEmpty):
                    (classUris, propertyUris, instanceUris) = autodetect.autodetectUris(store, vocabUri, userAgent)    
                    random.seed()
                    if autodetectUrisIfEmpty and not classUri and classUris:
                        classUri = random.choice(classUris)
                    if autodetectUrisIfEmpty and not propertyUri and propertyUris:
                        propertyUri = random.choice(propertyUris)
                    if autodetectUrisIfEmpty and not instanceUri and instanceUris:
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
                validatorOptions = options.ValidatorOptions(htmlVersions, defaultResponse, validateRDF, userAgent, client)
                
                recipes.checkRecipes(store, resourcesToCheck, validatorOptions)
                if classUri is not None:
                    namespaceFlavour = autodetect.autodetectNamespaceFlavour(vocabUri, classUri)
                    validRecipes = autodetect.autodetectValidRecipes(vocabUri, classUri, namespaceFlavour, htmlVersions)
                else:
                    namespaceFlavour = None
                    validRecipes = []
                
                if format == "html":        
                    store.parse(PATH_RDF_FILES + "/vapour.rdf")
                    store.parse(PATH_RDF_FILES + "/recipes.rdf")
                    store.parse(PATH_RDF_FILES + "/earl.rdf")        
                    store.parse(PATH_RDF_FILES + "/http.rdf")        
                    store.parse(PATH_RDF_FILES + "/vocab.rdf")        
                    model = common.createModel(store)
                    response = HttpResponse(strainer.resultsModelToHTML(model, vocabUri, classUri, propertyUri, instanceUri, True,
                                                                    autodetectUrisIfEmpty, 
                                                                    validatorOptions, namespaceFlavour, 
                                                                    validRecipes, resourceBaseUri, PATH_TEMPLATES),
                                            mimetype="text/html") #IE sucks
                    response["Vary"] = "Accept"
                    response["Access-Control-Allow-Origin"] = "*"
                    return response
                elif format == "rdf":
                    response = HttpResponse(store.serialize(format="pretty-xml"), mimetype="application/rdf+xml")
                    response["Vary"] = "Accept"
                    response["Access-Control-Allow-Origin"] = "*"
                    response["Content-Disposition"] = "attachment; filename=vapour.rdf"
                    response["Expires"] = "0"
                    response["Cache-Control"] = "must-revalidate, post-check=0, pre-check=0"
                    response["Pragma"] = "public"
                    return response
                else:
                    return HttpResponseBadRequest("<h1>Unknown format</h1> <p>Requested format '+ " + format + "'</p>")
            else:  # vocabUri is None
                return HttpResponse(strainer.justTheFormInHTML(resourceBaseUri, PATH_TEMPLATES))
        except Exception, e:
            logger.error(str(e))
            return HttpResponse(strainer.exceptionInHTML(e, resourceBaseUri, PATH_TEMPLATES), status=500)

