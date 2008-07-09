from rdflib import ConjunctiveGraph, URIRef
from httpdialog import followRedirects
import mimetypes
import httplib
from sets import Set
from vapour.namespaces import RDF, RDFS, OWL
from vapour.cup import common

HASH_NAMESPACE = { "name": "hash namespace" }
SLASH_NAMESPACE = { "name": "slash namespace" }

RECIPE1 = { "name": "Recipe 1", "link": "http://www.w3.org/TR/swbp-vocab-pub/#recipe1" }
RECIPE2 = { "name": "Recipe 2", "link": "http://www.w3.org/TR/swbp-vocab-pub/#recipe2" }
RECIPE3 = { "name": "Recipe 3", "link": "http://www.w3.org/TR/swbp-vocab-pub/#recipe3" }
RECIPE4 = { "name": "Recipe 4", "link": "http://www.w3.org/TR/swbp-vocab-pub/#recipe4" }
RECIPE5 = { "name": "Recipe 5", "link": "http://www.w3.org/TR/swbp-vocab-pub/#recipe5" }
RECIPE6 = { "name": "Recipe 6", "link": "http://www.w3.org/TR/swbp-vocab-pub/#recipe6" }

def autodetectUris(graph, vocabUri):
    contentType = mimetypes.rdfXml
    try:
        ( rootTestSubject, response ) = followRedirects( graph, "Derreferencing the vocabulary URI", vocabUri, contentType, method = "GET" )
    except Exception, e:
        raise Exception("Unable to autodetect URIs, the vocabulary cannot be retrieved (inner exception=" + str(e) + ")")

    if response.status == httplib.OK:
            tempGraph = ConjunctiveGraph()
            tempGraph.load( response )
            
            rdfsClasses = [x for x in tempGraph.subjects( RDF["type"], RDFS["Class"] )]
            owlClasses = [x for x in tempGraph.subjects( RDF["type"], OWL["Class"] )]        
            rdfProperties = [x for x in tempGraph.subjects( RDF["type"], RDF["Property"] )]
            objectProperties = [x for x in tempGraph.subjects( RDF["type"], OWL["ObjectProperty"] )]
            datatypeProperties = [x for x in tempGraph.subjects( RDF["type"], OWL["DatatypeProperty"] )]
            annotationProperties = [x for x in tempGraph.subjects( RDF["type"], OWL["AnnotationProperty"] )]
            owlOntologies = [x for x in tempGraph.subjects( RDF["type"], OWL["Ontology"] )]
            definedResources = [x for (x,y) in tempGraph.subject_objects( RDF["type"] ) ]
            
            # remove unwanted URIs
            owlClasses = filter( lambda x : not x.startswith( OWL ), owlClasses )
    
            allClasses = rdfsClasses + owlClasses
            allProperties = rdfProperties + objectProperties + datatypeProperties + annotationProperties
            allInstances = list(Set(definedResources) - Set(allClasses + allProperties + owlOntologies))
    
            classes = pickFromNamespaceIfPossible(allClasses, vocabUri)
            properties = pickFromNamespaceIfPossible(allProperties, vocabUri)
            instances = pickFromNamespaceIfPossible(allInstances, vocabUri)
            return ( classes, properties, instances )
    else:
            raise Exception("Unable to autodetect URIs, the vocabulary cannot be retrieved (response code=" + str( response.status ) + ")")

def pickFromNamespaceIfPossible(entities, namespace):
    definedInTheNamespace = filter ( lambda x : x.startswith(namespace), entities )
    if len(definedInTheNamespace) > 0:
        return definedInTheNamespace
    else:
        return entities
        
def autodetectNamespaceFlavour(vocabUri, oneResourceUri):
    # FIXME: this is a silly implementation
    if "#" in oneResourceUri:
        return HASH_NAMESPACE
    else:
        return SLASH_NAMESPACE
    
def autodetectValidRecipes(vocabUri, oneResourceUri, namespaceFlavour, htmlVersions):
    if not htmlVersions:
        # recipe 1 or 2
        if namespaceFlavour is HASH_NAMESPACE:
            return [RECIPE1]
        else:
            return [RECIPE2]
    else:
        # recipes 3 - 6
        if namespaceFlavour is HASH_NAMESPACE:
            return [RECIPE3]
        else:
            return [RECIPE4, RECIPE5, RECIPE6]

