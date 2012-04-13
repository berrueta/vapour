
import os
import sys
from rdflib import ConjunctiveGraph, Graph
from vapour.namespaces import *
import logging
from vapour.common.odict import OrderedDict
from vapour.settings import PATH_LOG

logging.basicConfig(level=logging.DEBUG, format="%(asctime)s %(filename)s:%(lineno)d %(levelname)s: %(message)s", stream=sys.stderr)

def createStore():
    store = Graph()
    store.bind('earl', EARL)
    store.bind('rdf', RDF)
    store.bind('rdfs', RDFS)
    store.bind('dc', DC)
    store.bind('dct', DCT)
    store.bind('uri', URI)
    store.bind('http', HTTP)
    store.bind('vapour', VAPOUR)
    store.bind('recipes', RECIPES)
    store.bind('foaf', FOAF)
    return store

def createModel(store):
    return store

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
        while (mime[0]==" "):
            mime = mime[1:]
        while (mime[-1]==" "):
            mime = mime[:-1]
        if not mimes.has_key(q):
            mimes[q] = []
        mimes[q].append(mime)

    mimes.sort()
    mimes.reverse()
    
    for q, mime in mimes.items():
        if ("application/xhtml+xml" in mime or "text/html" in mime):
            return "html"
        if ("application/rdf+xml" in mime):
            return "rdf"
    return "html"

