
from rdflib.Graph import ConjunctiveGraph
from rdflib.sparql.sparqlGraph import SPARQLGraph
from rdflib.sparql.graphPattern import GraphPattern
from rdflib.sparql import Query
from vapour.namespaces import *
from vapour.teapot import options
import httplib
import urllib
from Cheetah.Template import Template
import datetime
import sys
import traceback

try:
    import Cheetah
except ImportError:
    print >> stderr, "This program REQUIRES cheetah. Please install the library"
    sys.exit(-1)

try:
    import rdflib
except ImportError:
    print >>stderr, "This program REQUIRES rdflib. Please install the library"
    sys.exit(-1)


def getTestRequirements(model):
    sparqlGr = SPARQLGraph(model)
    select = ("?testRequirement", # 0
              "?testRequirementTitle", # 1
              "?testRequirementOrder", # 2 
              )
    where = GraphPattern([
         ("?testRequirement", RDF["type"], EARL["TestRequirement"]),
         ("?testRequirement", DC["title"], "?testRequirementTitle"),
         ("?testRequirement", VAPOUR_VOCAB["order"], "?testRequirementOrder")
         ])
    resultSet = Query.query(sparqlGr, select, where)
    # manually sorting the results
    sortByOrderAndTitleFunc = lambda x, y : cmp(x[2],y[2]) or cmp(x[1],y[1]) 
    resultSet.sort(sortByOrderAndTitleFunc)
    return resultSet

def isThereAnyFailingTest(model):
    sparqlGr = SPARQLGraph(model)
    where = GraphPattern([
        ("?assertion", RDF["type"], EARL["Assertion"]),
        ("?assertion", EARL["result"], "?result"),
        ("?result", EARL["validity"], EARL["fail"])
        ])
    return Query.queryObject(sparqlGr, where).ask()

def getResultsFromModel(model, testRequirementUri):
    sparqlGr = SPARQLGraph(model)
    select = ("?assertion", #0
              "?test", # 1
              "?testTitle", # 2
              "?validity", # 3
              "?validityLabel", # 4
              "?subject", # 5
              "?subjectTitle") # 6
    where = GraphPattern([          
        ("?assertion", RDF["type"], EARL["Assertion"]),
        (testRequirementUri, DCT["hasPart"], "?assertion"),
        ("?assertion", EARL["test"], "?test"),
        ("?test", DC["title"], "?testTitle"),
        ("?assertion", EARL["result"], "?result"),
        ("?result", EARL["validity"], "?validity"),
        ("?validity", RDFS["label"], "?validityLabel"),
        ("?assertion", EARL["subject"], "?subject"),
        ("?subject", DC["title"], "?subjectTitle")
        ])
    results = Query.query(sparqlGr, select, where)
    # manually sorting the results
    sortBySubjectAndTestCase = lambda x, y : cmp(x[6],y[6]) or cmp(x[2],y[2])
    results.sort(sortBySubjectAndTestCase)    
    return results

def getHttpTracesFromModel(model, testRequirementUri):
    sparqlGr = SPARQLGraph(model)
    select = (
              "?testSub", # 0
              "?testSubTitle", # 1
              "?absoluteUri", # 2

              "?statusCodeNumber", # 3
              "?responseContentType", # 4
              "?responseLocation",  # 5

              "?statusCodeTest", # 6
              "?statusCodeValidity", # 7
              "?responseContentTypeTest", # 8
              "?responseContentTypeValidity", # 9
              
              "?requestAccept", # 10
              "?previousRequestCount", # 11
              "?requestType", # 12 <-- unused
              "?requestMethodName", #13
              "?requestAbsPath", #14
              "?requestHost", #15
              "?responseVary", #16
              "?userAgent" #17
              )
    where = GraphPattern([
        (testRequirementUri, DCT["hasPart"], "?assertion"),
        ("?assertion", EARL["subject"], "?testSub"),
        ("?testSub", RDF["type"], EARL["TestSubject"]),
        ("?testSub", DC["title"], "?testSubTitle"),
        ("?testSub", EARL["httpRequest"], "?request"),
        ("?request", HTTP["absoluteURI"], "?absoluteUri"),
        ("?testSub", EARL["httpResponse"], "?response"),
        ("?response", HTTP["statusCodeNumber"], "?statusCodeNumber"),
        ("?request", RDF["type"], "?requestType"),
        ("?request", HTTP["methodName"], "?requestMethodName"),
        ("?request", HTTP["abs_path"], "?requestAbsPath"),
        ("?request", HTTP["host"], "?requestHost"),
        ("?testSub", VAPOUR_VOCAB["previousRequestCount"], "?previousRequestCount")
    ])
    optional = [
        GraphPattern([("?request", HTTP["accept"], "?requestAccept")]),
        GraphPattern([("?request", HTTP["user-agent"], "?userAgent")]),
        GraphPattern([("?response", HTTP["content-type"], "?responseContentType")]),
        GraphPattern([("?response", HTTP["location"], "?responseLocation")]),
        GraphPattern([("?response", HTTP["vary"], "?responseVary")]),
        GraphPattern([
                      ("?statusCodeAssertion", EARL["subject"], "?testSub"),
                      ("?statusCodeAssertion", EARL["test"], "?statusCodeTest"),
                      ("?statusCodeTest", VAPOUR_VOCAB["propertyUnderTest"], HTTP["statusCodeNumber"]),
                      ("?statusCodeAssertion", EARL["result"], "?statusCodeResult"),
                      ("?statusCodeResult", EARL["validity"], "?statusCodeValidity")
        ]),
        GraphPattern([
                      ("?responseContentTypeAssertion", EARL["subject"], "?testSub"),
                      ("?responseContentTypeAssertion", EARL["test"], "?responseContentTypeTest"),
                      ("?responseContentTypeTest", VAPOUR_VOCAB["propertyUnderTest"], HTTP["content-type"]),
                      ("?responseContentTypeAssertion", EARL["result"], "?responseContentTypeResult"),
                      ("?responseContentTypeResult", EARL["validity"], "?responseContentTypeValidity")
        ])
    ]
    results = [x for x in Query.query(sparqlGr, select, where, optional)]
    # manually sorting the results
    sortByPreviousRequestCount = lambda x, y : cmp(x[11],y[11]) 
    results.sort(sortByPreviousRequestCount)    
    return results

def getFinalUriFromModel(model, testRequirementUri):
    sparqlGr = SPARQLGraph(model)
    select = ("?finalUri", "?contentType", "?statusCodeNumber")
    # FIXME: a FILTER clause should be added to check the statusCodeNumber == 200
    where = GraphPattern([
        (testRequirementUri, DCT["hasPart"], "?assertion"),
        ("?assertion", EARL["subject"], "?testSubject"),
        ("?testSubject", EARL["httpRequest"], "?getRequest"),
        ("?testSubject", EARL["httpResponse"], "?httpResponse"),
        ("?httpResponse", HTTP["content-type"], "?contentType"),
        ("?httpResponse", HTTP["statusCodeNumber"], "?statusCodeNumber"),
        ("?getRequest", HTTP["absoluteURI"], "?finalUri")
    ])
    return [x for x in Query.query(sparqlGr, select, where) if int(x[2]) == httplib.OK]

def getHttpRange14ConclusionsFromModel(model, testRequirementUri):
    sparqlGr = SPARQLGraph(model)
    select = ("?resource", # 0
              "?resourceType", #1
              "?resourceTypeLabel" # 2
    )
    where = GraphPattern([
        (testRequirementUri, DCT["hasPart"], "?assertion"),
        ("?assertion", EARL["subject"], "?testSubject"),
        ("?testSubject", VAPOUR_VOCAB["httpRange14ConclusionOn"], "?resource"),
        ("?resource", RDF["type"], "?resourceType"),
        ("?resourceType", RDFS["label"], "?resourceTypeLabel")
    ])
    results = [x for x in Query.query(sparqlGr, select, where)]
    # manually sorting the results
    sortByUri = lambda x, y : cmp(x[0],y[0]) 
    results.sort(sortByUri)    
    return results

def getTestAgent(model):
    """
    Determine the software agent that was used to execute the tests
    """
    sparqlGr = SPARQLGraph(model)
    select = ("?agent", # 0
              "?agentTitle", # 1
              "?agentVersion", # 2
              "?agentHomepage" # 3
              )
    where = GraphPattern([
       ("?x", EARL["assertedBy"], "?agent"),
       ("?agent", DC["title"], "?agentTitle"),
       ("?agent", DCT["hasVersion"], "?agentVersion"),
       ("?agent", FOAF["homepage"], "?agentHomepage")
    ])
    results = Query.query(sparqlGr, select, where)
    return [x for x in results][0]

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
                       resourceBaseUri = "resources", templateDir = "templates"):
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

def justTheFormInHTML(resourceBaseUri = "resources", templateDir = "templates"):    
    validatorOptions = options.ValidatorOptions()
    data = prepareData(resourceBaseUri, printForm = True, validatorOptions = validatorOptions)
    t = Template(file=templateDir + "/results.tmpl", searchList=[data])
    return t

def exceptionInHTML(e, resourceBaseUri = "resources", templateDir = "templates"):
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
    from rdflib.Graph import ConjunctiveGraph, Graph
    from rdflib.sparql import sparqlGraph
    
    store = Graph()
    store.parse("../../../../../webpage/vapour.rdf")
    store.parse("../../../../../webpage/recipes.rdf")
    store.parse("../../../../../webpage/earl.rdf")
    store.parse("../../../../../webpage/demo-report5.rdf")
    model = sparqlGraph.SPARQLGraph(store)
    t = resultsModelToHTML(model)
    print t

