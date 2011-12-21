
import rdflib
from rdflib.graph import ConjunctiveGraph, Graph
rdflib.plugin.register("sparql", rdflib.query.Processor, "rdfextras.sparql.processor", "Processor")
rdflib.plugin.register("sparql", rdflib.query.Result, "rdfextras.sparql.query", "SPARQLQueryResult")
from vapour.namespaces import *
from vapour.teapot import options
import httplib
import urllib
from Cheetah.Template import Template
import datetime
import sys
import traceback

templateDir = "vapour/strainer/templates/" #FIXME

def getTestRequirements(model):
    query = """
        SELECT ?testRequirement ?testRequirementTitle ?testRequirementOrder
        WHERE {
            ?testRequirement rdf:type earl:TestRequirement .
            ?testRequirement dc:title ?testRequirementTitle .
            ?testRequirement vapour:order ?testRequirementOrder .            
        }
        ORDER BY ?testRequirementOrder ?testRequirementTitle
    """
    return model.query(query, initNs=bindings)

def isThereAnyFailingTest(model):
    query = """
        ASK
        WHERE {
            ?assertion rdf:type earl:Assertion .
            ?assertion earl:result ?result .
            ?result earl:outcome earl:failed .
        }
    """
    return model.query(query, initNs=bindings)

def getResultsFromModel(model, testRequirementUri):
    query = """
        SELECT ?assertion ?test ?testTitle ?outcome ?outcomeLabel ?subject ?subjectTitle
        WHERE {      
            ?assertion rdf:type earl:Assertion .
            <%s> dct:hasPart ?assertion .
            ?assertion earl:test ?test .
            ?test dc:title ?testTitle .
            ?assertion earl:result ?result .
            ?result  earl:outcome ?outcome .
            ?outcome dc:title ?outcomeLabel .
            ?assertion earl:subject ?subject .
            ?subject dc:title ?subjectTitle .
        }
        ORDER BY ?subjectTitle ?testTitle
    """ % testRequirementUri
    return model.query(query, initNs=bindings)

def getHttpTracesFromModel(model, testRequirementUri):
    query = """
        SELECT ?response ?responseTitle ?absoluteUri ?statusCodeNumber ?responseContentType ?responseLocation
               ?statusCodeTest ?statusCodeValidity ?responseContentTypeTest ?responseContentTypeValidity
               ?requestAccept ?previousRequestCount ?requestType ?requestMethodName ?requestAbsPath
               ?requestHost ?responseVary ?userAgent
        WHERE {
            <%s> dct:hasPart ?assertion .
            ?assertion earl:subject ?response .
            ?response rdf:type earl:TestSubject ;
              dc:title ?responseTitle ;
              http:statusCodeNumber ?statusCodeNumber ;
              vapour:previousRequestCount ?previousRequestCount .
            ?request http:response ?response ;
              http:absoluteURI ?absoluteUri ;
              http:type ?requestType ;
              http:methodName ?requestMethodName ;
              http:abs_path ?requestAbsPath ;
              http:host ?requestHost .
            OPTIONAL { ?request http:accept ?requestAccept . }
            OPTIONAL { ?request http:user-agent ?userAgent . }
            OPTIONAL { ?response http:content-type ?responseContentType . }
            OPTIONAL { ?response http:location ?responseLocation . }
            OPTIONAL { ?response http:vary ?responseVary . }
            OPTIONAL {
                        ?statusCodeAssertion earl:subject ?response .
                        ?statusCodeAssertion earl:test ?statusCodeTest .
                        ?statusCodeTest earl:propertyUnderTest http:statusCodeNumber .
                        ?statusCodeAssertion earl:result ?statusCodeResult .
                        ?statusCodeResult earl:outcome ?statusCodeValidity .
            }
            OPTIONAL {
                        ?responseContentTypeAssertion earl:subject ?response .
                        ?responseContentTypeAssertion earl:test ?responseContentTypeTest .
                        ?responseContentTypeTest vapour:propertyUnderTest http:content-type .
                        ?responseContentTypeAssertion earl:result ?responseContentTypeResult .
                        ?responseContentTypeResult earl:outcome ?responseContentTypeValidity .
            }
        }
        ORDER BY ?previousRequestCount
    """ % testRequirementUri
    return model.query(query, initNs=bindings)

def getFinalUriFromModel(model, testRequirementUri):
    query = """
        SELECT ?finalUri ?contentType ?statusCodeNumber 
        WHERE {
          <%s> dct:hasPart ?assertion .
          ?assertion earl:subject ?response .
          ?getRequest http:response ?response .
          ?response http:content-type ?contentType .
          ?response http:statusCodeNumber ?statusCodeNumber .
          ?getRequest http:absoluteURI ?finalUri .
          FILTER (?statusCodeNumber = 200)
    }
    """ % testRequirementUri
    return model.query(query, initNs=bindings)

def getHttpRange14ConclusionsFromModel(model, testRequirementUri):
    query = """
        SELECT ?resource ?resourceType ?resourceTypeLabel
        WHERE {
          <%s> dct:hasPart ?assertion .
          ?assertion earl:subject ?response .
          ?response vapour:httpRange14ConclusionOn ?resource .
          ?resource rdf:type ?resourceType .
          ?resourceType rdfs:label ?resourceTypeLabel .
        }
        ORDER BY ?resource
    """ % testRequirementUri
    return model.query(query, initNs=bindings)

def getTestAgent(model):
    """
    Determine the software agent that was used to execute the tests
    """
    query = """ 
        SELECT ?agent ?agentTitle ?agentVersion ?agentHomepage
        WHERE {
          ?x earl:assertedBy ?agent .
          ?agent dc:title ?agentTitle ;
            dct:hasVersion ?agentVersion ;
            foaf:homepage ?agentHomepage .
        }
    """
    return model.query(query, initNs=bindings)

def sortTrace(trace):    
    # FIXME
    return trace

def prepareData(resourceBaseUri, validatorOptions, vocabUri="", classUri="", propertyUri="", instanceUri = "", printForm=False, autodetectUris=False, namespaceFlavour=None, validRecipes=[]):
    data = {}
    
    data['resourceBaseUri'] = resourceBaseUri
    
    data['printForm'] = printForm
    data['vocabUri'] = vocabUri
    data['classUri'] = classUri
    data['propertyUri'] = propertyUri
    data['instanceUri'] = instanceUri
    data['autodetectUris'] = autodetectUris
    data['validateRDF'] = validatorOptions.validateRdf
    data['htmlVersions'] = validatorOptions.htmlVersions
    data['defaultResponse'] = validatorOptions.defaultResponse
    data['userAgent'] = validatorOptions.userAgent
    data['namespaceFlavour'] = namespaceFlavour
    data['validRecipes'] = validRecipes
    
    data['testAgent'] = {} # it may be overwritten later
    data['testRequirements'] = {} # it may be overwritten later
    
    data['testResults'] = {}
    data['httpTraces'] = {}
    data['finalUris'] = {}
    data['httpRange14Conclusions'] = {}
    data['rdfReportUrl'] = '?'+ str(urllib.urlencode({'vocabUri':vocabUri or '','classUri':classUri or '','autodetectUris':str(int(autodetectUris)),'propertyUri':propertyUri or '','validateRDF':str(int(validatorOptions.validateRdf)),'htmlVersions':str(int(validatorOptions.htmlVersions)),'format':'rdf', 'defaultResponse':validatorOptions.defaultResponse})).replace("&","&amp;")
    return data

def resultsModelToHTML(model, vocabUri, classUri, propertyUri, instanceUri, printForm,
                       autodetectUris, 
                       validatorOptions, namespaceFlavour, validRecipes,
                       resourceBaseUri = "resources", templateDir = templateDir):
    """
    Entry point: use a RDFmodel with results as input to populate a
    cheetah template
    """
    data = prepareData(resourceBaseUri, validatorOptions, vocabUri, classUri, propertyUri, instanceUri, printForm, autodetectUris, namespaceFlavour, validRecipes)
    data['testRequirements'] = getTestRequirements(model)
    for testRequirementUri in [x[0] for x in data['testRequirements']]:        
        data['testResults'][testRequirementUri] = getResultsFromModel(model, testRequirementUri)
        data['httpTraces'][testRequirementUri] = sortTrace(getHttpTracesFromModel(model, testRequirementUri))
        data['finalUris'][testRequirementUri] = getFinalUriFromModel(model, testRequirementUri)
        data['httpRange14Conclusions'][testRequirementUri] = getHttpRange14ConclusionsFromModel(model, testRequirementUri)
    data['testAgent'] = getTestAgent(model)
    data['isThereAnyFailingTest'] = isThereAnyFailingTest(model)
    data['reportDate'] = str(datetime.datetime.now())
    t = Template(file=templateDir + "/results.tmpl", searchList=[data])
    return t

def justTheFormInHTML(resourceBaseUri = "resources", templateDir = templateDir):    
    validatorOptions = options.ValidatorOptions()
    data = prepareData(resourceBaseUri, printForm = True, validatorOptions = validatorOptions)
    t = Template(file=templateDir + "/results.tmpl", searchList=[data])
    return t

def exceptionInHTML(e, resourceBaseUri = "resources", templateDir = templateDir):
    data = {}
    data['resourceBaseUri'] = resourceBaseUri
    data['exceptionDescription'] = str(e)
    data['exceptionDetails'] = ""
    for msg in traceback.format_tb(sys.exc_info()[2]):
        data['exceptionDetails'] += str(msg)
    t = Template(file=templateDir + "/exception.tmpl", searchList=[data])
    return t

if __name__ == "__main__":
    #
    # Test with local files
    #
    store = Graph()
    store.parse("../../../../../webpage/vapour.rdf")
    store.parse("../../../../../webpage/recipes.rdf")
    store.parse("../../../../../webpage/earl.rdf")
    store.parse("../../../../../webpage/demo-report5.rdf")
    model = sparqlGraph.SPARQLGraph(store)
    t = resultsModelToHTML(model)
    print t

