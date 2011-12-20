from rdflib import Namespace

EARL = Namespace("http://www.w3.org/ns/earl#")
RDF = Namespace("http://www.w3.org/1999/02/22-rdf-syntax-ns#")
RDFS = Namespace("http://www.w3.org/2000/01/rdf-schema#")
OWL = Namespace("http://www.w3.org/2002/07/owl#")
DC = Namespace("http://purl.org/dc/elements/1.1/")
DCT = Namespace("http://purl.org/dc/terms/")
URI = Namespace("http://www.w3.org/2006/uri#")
HTTP = Namespace("http://www.w3.org/2006/http#")
HTTP_METHODS = Namespace("http://www.w3.org/2006/http-methods#")
HTTP_STATUS_CODES = Namespace("http://www.w3.org/2006/http-statusCodes#")
VAPOUR_VOCAB = Namespace("http://vapour.sourceforge.net/vocab.rdf#")
VAPOUR_SOFT = Namespace("http://vapour.sourceforge.net/vapour.rdf#")
RECIPES = Namespace("http://vapour.sourceforge.net/recipes.rdf#")
FOAF = Namespace("http://xmlns.com/foaf/0.1/")

bindings = { 
                u"earl":EARL,
                u"rdf":RDF,
                u"rdfs":RDFS,
                u"owl":OWL,
                u"dc":DC,
                u"dct":DCT,
                u"uri":URI,
                u"http":HTTP,
                u"vapourv":VAPOUR_VOCAB,
                u"vapours":VAPOUR_SOFT,
                u"recipes":RECIPES,
                u"foaf":FOAF,
            }

