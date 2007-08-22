from rdflib import ConjunctiveGraph, URIRef
from httpdialog import followRedirects
import mimetypes
import httplib
from vapour.namespaces import RDF, RDFS, OWL

def autodetectUris(graph, vocabUri):
    contentType = mimetypes.rdfXml
    try:
        (rootTestSubject, response) = followRedirects(graph, "Derreferencing the vocabulary URI", vocabUri, contentType)
        if response.status == httplib.OK:
            tempGraph = ConjunctiveGraph()
            tempGraph.load(response)
            
            rdfsClasses = [x for x in tempGraph.subjects(RDF["type"], RDFS["Class"])]
            owlClasses = [x for x in tempGraph.subjects(RDF["type"], OWL["Class"])]        
            rdfProperties = [x for x in tempGraph.subjects(RDF["type"], RDF["Property"])]
            objectProperties = [x for x in tempGraph.subjects(RDF["type"], OWL["ObjectProperty"])]
            datatypeProperties = [x for x in tempGraph.subjects(RDF["type"], OWL["DatatypeProperty"])]
            annotationProperties = [x for x in tempGraph.subjects(RDF["type"], OWL["AnnotationProperty"])]
            
            # remove unwanted URIs
            owlClasses = filter(lambda x : not x.startswith(OWL), owlClasses)
    
            classes = rdfsClasses + owlClasses
            properties = rdfProperties + objectProperties + datatypeProperties + annotationProperties
            return (classes, properties)
        else:
            print "WARNING: Unable to autodetect URIs, the vocabulary cannot be retrieved (response code=", str(response.status), ")"
            return (None, None)
    except Exception, e:
        print "WARNING: Unable to autodetect URIs, the vocabulary cannot be retrieved (exception=", e, ")"
        return (None, None)
        
