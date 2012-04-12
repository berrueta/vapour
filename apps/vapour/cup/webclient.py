
import logging
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

        uri = None
        uri = request.GET.get("uri")
        if (not uri):
            uri = request.GET.get("vocabUri") # legacy http api
        if (uri is "" or uri is "http://"): 
            uri = None

        defaultResponse = "dontmind"
        defaultResponse = request.GET.get("defaultResponse")
        if ((defaultResponse is not "rdfxml") and (defaultResponse is not "html") and (defaultResponse is not "dontmind")):
            defaultResponse = "dontmind" # default value            

        userAgent = options.defaultUserAgent
        userAgent = request.META["HTTP_USER_AGENT"]
        if (not userAgent):
            userAgent = options.defaultUserAgent
        elif ("\n" in userAgent):
            userAgent = options.defaultUserAgent # prevent HTTP header injection

        format = "html"
        paramFormat = request.GET.get("format")
        if (paramFormat and (paramFormat in ["rdf", "html"])):
            format = paramFormat
            logger.info("Using forced format to return the report as %s" % format.upper())
        elif ((uri is not None) and (request.META.has_key("HTTP_ACCEPT"))):
            format = common.getBestFormat(request.META["HTTP_ACCEPT"])
            logger.info("Using content negotiation to return the report as %s" % format.upper())

        client = request.META.get('REMOTE_ADDR')

        if (request.GET.get("mixedAccept")):
            mixedAccept = bool(int(request.GET.get("mixedAccept"))) 
        else:
            mixedAccept = False

        if (request.GET.get("validateRDF")):
            validateRDF = bool(int(request.GET.get("validateRDF"))) 
        else:
            validateRDF = False

        if (request.GET.get("htmlVersions")):
            htmlVersions = bool(int(request.GET.get("htmlVersions"))) 
        else:
            htmlVersions = False         

        try:
            store = common.createStore()
                
            if uri is not None:
                if (client):
                    logger.info("Request from %s over URI: %s" % (client, uri))
                else:
                    logger.info("Request over URI: " + uri)

                resourceToCheck = {'uri': uri, 'description': "resource URI", 'order': 1} #FIXME: not necessary anymore, but it'd need some code rewriting          

                # defines the options of the validator
                validatorOptions = options.ValidatorOptions(htmlVersions, defaultResponse, mixedAccept, validateRDF, userAgent, client)
                
                recipes.checkRecipes(store, resourceToCheck, validatorOptions)
                namespaceFlavour = None
                validRecipes = []
                
                if format == "html":        
                    store.parse(PATH_RDF_FILES + "/vapour.rdf")
                    store.parse(PATH_RDF_FILES + "/recipes.rdf")
                    store.parse(PATH_RDF_FILES + "/earl.rdf")        
                    store.parse(PATH_RDF_FILES + "/http.rdf")        
                    store.parse(PATH_RDF_FILES + "/vocab.rdf")        
                    model = common.createModel(store)
                    response = HttpResponse(strainer.resultsModelToHTML(model, uri, True,
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

