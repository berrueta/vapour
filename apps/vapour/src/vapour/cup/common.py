import os
from rdflib.Graph import ConjunctiveGraph, Graph
from vapour.namespaces import *
from rdflib.sparql import sparqlGraph
import logging

pathToRdfFiles = "http://vapour.sourceforge.net"
pathToTemplates = "../strainer/templates" 
pathToLog = "../../../log/vapour.log"  

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
    global pathToTemplates
    if os.environ.get("VAPOUR_TEMPLATES"):
        pathToTemplates = os.environ.get("VAPOUR_TEMPLATES")
    global pathToLog
    if os.environ.get("VAPOUR_LOG"):
        pathToLog = os.environ.get("VAPOUR_LOG")

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

