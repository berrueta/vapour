
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
            uri = request.GET.get("uri")
        except KeyError:
            try:
                uri = request.GET.get("vocabUri") # legacy http interface
            except KeyError:
                uri = None
        finally:
            if (uri == "" or uri == "http://"): uri = None

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
            if ((uri is not None) and (request.META.has_key("HTTP_ACCEPT"))):
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
            store = common.createStore()
                
            if uri is not None:
                if (client):
                    logger.info("Request from %s over URI: %s" % (client, uri))
                else:
                    logger.info("Request over URI: " + uri)

                resourceToCheck = {'uri': uri, 'description': "resource URI", 'order': 1} #FIXME: not necessary anymore, but it'd need some code rewriting          

                # defines the options of the validator
                validatorOptions = options.ValidatorOptions(htmlVersions, defaultResponse, validateRDF, userAgent, client)
                
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

