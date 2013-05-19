
import random, traceback
from datetime import datetime
from django.http import HttpResponse, HttpResponseBadRequest
from vapour.strainer import strainer
from vapour.teapot import recipes, autodetect, options
from vapour.cup import common
from vapour.settings import STATIC_URL, PATH_TEMPLATES, PATH_RDF_FILES
from vapour.common.lang import if_else
from vapour.common import getLogger

import warnings
warnings.simplefilter("ignore", DeprecationWarning)

resourceBaseUri = if_else(STATIC_URL[-1] == "/", STATIC_URL[:-1], STATIC_URL) #remove last slash

class cup:

    @staticmethod
    def GET(request):

        logger = getLogger()

        uri = request.GET.get("uri")
        if (not uri):
            uri = request.GET.get("vocabUri") # legacy http api
        if (uri is "" or uri is "http://"): 
            uri = None

        defaultResponse = "dontmind"
        defaultResponse = request.GET.get("defaultResponse")
        if ((defaultResponse is not "rdfxml") and (defaultResponse is not "html") and (defaultResponse is not "dontmind")):
            defaultResponse = "dontmind" # default value            

        userAgent = request.GET.get("userAgent")
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

        if (request.GET.get("validateRDF")):
            validateRDF = bool(int(request.GET.get("validateRDF"))) 
        else:
            validateRDF = False

        if (request.GET.get("htmlVersions")):
            htmlVersions = bool(int(request.GET.get("htmlVersions"))) 
        else:
            htmlVersions = False   

        if (request.GET.get("mixedAccept")):
            mixedAccept = bool(int(request.GET.get("mixedAccept"))) 
        else:
            mixedAccept = False      

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
                
                startTime = datetime.now()
                recipes.checkRecipes(store, resourceToCheck, validatorOptions)
                dialogTime = datetime.now() - startTime
                namespaceFlavour = None
                validRecipes = []
                
                logger.debug("Reading common files from %s" % PATH_RDF_FILES)
                store.parse(PATH_RDF_FILES + "/vapour.rdf")
                store.parse(PATH_RDF_FILES + "/recipes.rdf")
                store.parse(PATH_RDF_FILES + "/earl.rdf")        
                store.parse(PATH_RDF_FILES + "/http.rdf")        
                store.parse(PATH_RDF_FILES + "/vocab.rdf")       
                model = common.createModel(store)

                responseTime = datetime.now() - startTime

                logger.info("Response time: %d (ms) - HTTP dialog time: %d (ms)" % (responseTime.total_seconds() * 1000,
                                                                                    dialogTime.total_seconds() * 1000))

                if format == "html":
                    responseTimeSeconds = round(responseTime.total_seconds() * 1000) / 1000;
                    response = HttpResponse(strainer.resultsModelToHTML(model, uri, True,
                                                                        validatorOptions, namespaceFlavour, 
                                                                        validRecipes, responseTimeSeconds,
                                                                        resourceBaseUri, PATH_TEMPLATES),
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

