import os
import sys
from rdflib.Graph import ConjunctiveGraph, Graph
from vapour.namespaces import *
from rdflib.sparql import sparqlGraph
import logging
from vapour.common.odict import OrderedDict

pathToRdfFiles = "http://vapour.sourceforge.net"
pathToTemplates = "../strainer/templates" 
pathToLog = "../../../log/vapour.log"  
allowIntranet = False

logging.basicConfig(level=logging.DEBUG, format="%(asctime)s %(levelname)s: %(message)s", stream=sys.stderr)

def createStore():
    store = Graph()
    store.bind('earl', EARL)
    store.bind('rdf', RDF)
    store.bind('rdfs', RDFS)
    store.bind('dc', DC)
    store.bind('dct', DCT)
    store.bind('uri', URI)
    store.bind('http', HTTP)
    store.bind('vapourv', VAPOUR_VOCAB)
    store.bind('vapour', VAPOUR_SOFT)
    store.bind('recipes', RECIPES)
    store.bind('foaf', FOAF)
    return store

def createModel(store):
    return sparqlGraph.SPARQLGraph(store)

def readEnvironment():
    global pathToRdfFiles
    if os.environ.get("VAPOUR_RDF_FILES"):
        pathToRdfFiles = os.environ.get("VAPOUR_RDF_FILES")        
    logging.debug("Path to RDF files (VAPOUR_RDF_FILES): " + pathToRdfFiles)
    global pathToTemplates
    if os.environ.get("VAPOUR_TEMPLATES"):
        pathToTemplates = os.environ.get("VAPOUR_TEMPLATES")
    logging.debug("Path to templates (VAPOUR_TEMPLATES): " + pathToTemplates)
    global pathToLog
    if os.environ.get("VAPOUR_LOG"):
        pathToLog = os.environ.get("VAPOUR_LOG")
    logging.debug("Path to log file (VAPOUR_LOG): " + pathToLog)
    global allowIntranet
    if os.environ.get("VAPOUR_ALLOW_INTRANET"):
        allowIntranet = os.environ.get("VAPOUR_ALLOW_INTRANET") is "1"
    logging.debug("Allow intranet addresses? (VAPOUR_ALLOW_INTRANET): " + str(allowIntranet))

def clearLoggerHandlers(logger):
	#because logger prints duplicate message, and I don't know how to fix it
	handlers = logger.handlers
	for handler in handlers:
		logger.removeHandler(handler)
	return logger

def createLogger(name='vapour'):
	logger = logging.getLogger(name)
	logger = clearLoggerHandlers(logger) #FIXME
	hdlr = logging.FileHandler(pathToLog)
	formatter = logging.Formatter('%(asctime)s %(levelname)s: %(message)s')
	hdlr.setFormatter(formatter)
	logger.addHandler(hdlr)
	logger.setLevel(logging.INFO)
	return logger

def getBestFormat(accceptHeader):
    #Example: text/xml,application/xml,application/xhtml+xml,text/html;q=0.9,text/plain;q=0.8,image/png,*/*;q=0.5
    mimes = OrderedDict()
    for one in accceptHeader.split(","):
        mime = None
        q = None
        splitted = one.split(";")
        if (len(splitted)>1):
            mime = splitted[0]
            q = float(splitted[1].split("=")[1])
        else:
            mime = splitted[0]
            q = float("1.0")

        if not mimes.has_key(q):
            mimes[q] = []

        mimes[q].append(mime)

    mimes.sort()
    mimes.reverse()
    
    for key in mimes.keys():
        if ("text/html" in mimes[key] or "application/xhtml+xml" in mimes[key]):
            return "html"
        if ("application/rdf+xml" in mimes[key]):
            return "rdf"

    return "html" #FIXME

