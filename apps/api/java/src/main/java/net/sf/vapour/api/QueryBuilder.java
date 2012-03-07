package net.sf.vapour.api;

class QueryBuilder {
	
	public static String buildAskFailedTests() {
		StringBuilder sb = new StringBuilder();
		sb.append("PREFIX earl: <http://www.w3.org/ns/earl#> \n");
		sb.append("PREFIX dc: <http://purl.org/dc/elements/1.1/> \n");
		sb.append("ASK { \n");
		sb.append("  ?testRequirement a earl:TestRequirement ; \n");
		sb.append("    dc:hasPart ?assertion . \n");
		sb.append("  ?assertion a earl:Assertion . \n");
        sb.append("  ?assertion earl:result ?result . \n");
        sb.append("  ?result earl:outcome earl:failed . \n");
		sb.append("}");
		return sb.toString();
	}
	
	public static String buildCountTests() {
		StringBuilder sb = new StringBuilder();
		sb.append("PREFIX earl: <http://www.w3.org/ns/earl#> \n");
		sb.append("PREFIX dc: <http://purl.org/dc/elements/1.1/> \n");
		sb.append("SELECT (COUNT(DISTINCT ?testRequirement) AS ?count) \n");
		sb.append("WHERE { \n");
		sb.append("  ?testRequirement a earl:TestRequirement . \n");
		sb.append("  ?testRequirement dc:title ?testRequirementTitle . \n");
		sb.append("}");
		return sb.toString();
	}
	
	public static String buildCountFailedTests() {
		StringBuilder sb = new StringBuilder();
		sb.append("PREFIX earl: <http://www.w3.org/ns/earl#> \n");
		sb.append("PREFIX dc: <http://purl.org/dc/elements/1.1/> \n");
		sb.append("SELECT (COUNT(DISTINCT ?testRequirement) AS ?count) \n");
		sb.append("WHERE { \n");
		sb.append("  ?testRequirement a earl:TestRequirement ; \n");
		sb.append("    dc:hasPart ?assertion . \n");
		sb.append("  ?assertion a earl:Assertion . \n");
        sb.append("  ?assertion earl:result ?result . \n");
        sb.append("  ?result earl:outcome earl:failed . \n");
		sb.append("}");
		return sb.toString();
	}
	
	public static String buildGetTests() {
		StringBuilder sb = new StringBuilder();
		sb.append("PREFIX earl: <http://www.w3.org/ns/earl#> \n");
		sb.append("PREFIX dc: <http://purl.org/dc/elements/1.1/> \n");
		sb.append("PREFIX vapour: <http://vapour.sourceforge.net/vocab.rdf#> \n");
		sb.append("SELECT ?testRequirement ?testRequirementTitle ?testRequirementOrder \n");
		sb.append("WHERE { \n");
		sb.append("  ?testRequirement a earl:TestRequirement . \n");
		sb.append("  ?testRequirement dc:title ?testRequirementTitle . \n");
		sb.append("  ?testRequirement vapour:order ?testRequirementOrder . \n");           
		sb.append("} \n");
		sb.append("ORDER BY ?testRequirementOrder ?testRequirementTitle ");
		return sb.toString();
	}

	public static String buildDescribe(String uri) {
		StringBuilder sb = new StringBuilder();
		sb.append("DESCRIBE <");
		sb.append(uri);
		sb.append("> ");
		return sb.toString();
	}
	
	public static String buildAskFailedTest(String test) {
		StringBuilder sb = new StringBuilder();
		sb.append("PREFIX earl: <http://www.w3.org/ns/earl#> \n");
		sb.append("PREFIX dc: <http://purl.org/dc/elements/1.1/> \n");
		sb.append("ASK { \n");
		sb.append("  <" + test + "> a earl:TestRequirement ; \n");
        sb.append("    dc:hasPart ?assertion . \n");
        sb.append("  ?assertion earl:result ?result . \n");
        sb.append("  ?result earl:outcome earl:failed . \n");
		sb.append("}");
		return sb.toString();
	}
	
	public static String buildGetTestFinalUri(String test) {
		StringBuilder sb = new StringBuilder();
		sb.append("PREFIX earl: <http://www.w3.org/ns/earl#> \n");
		sb.append("PREFIX dct: <http://purl.org/dc/terms/> \n");
		sb.append("PREFIX http: <http://www.w3.org/2006/http#> \n");
		sb.append("SELECT ?finalUri ?contentType \n");
		sb.append("WHERE { \n");
		sb.append("  <" + test + "> dct:hasPart ?assertion . \n");
		sb.append("  ?assertion earl:subject ?response . \n");
		sb.append("  ?getRequest http:response ?response . \n");
		sb.append("  ?response http:content-type ?contentType . \n");
		sb.append("  ?response http:statusCodeNumber ?statusCodeNumber . \n");
		sb.append("  ?getRequest http:absoluteURI ?finalUri . \n");
		sb.append("  FILTER (?statusCodeNumber = 200) \n");
		sb.append("}");
		return sb.toString();
	}

	public static String buildGetTestAssertions(String test) {
		StringBuilder sb = new StringBuilder();
		sb.append("PREFIX earl: <http://www.w3.org/ns/earl#> \n");
		sb.append("PREFIX dc: <http://purl.org/dc/elements/1.1/> \n");
		sb.append("PREFIX dct: <http://purl.org/dc/terms/> \n");
		sb.append("PREFIX http: <http://www.w3.org/2006/http#> \n");
		sb.append("SELECT ?assertion ?test ?testTitle ?outcome ?outcomeLabel ?subject ?subjectTitle \n");
		sb.append("WHERE { \n");
		sb.append("  ?assertion a earl:Assertion . \n");
		sb.append("  <" + test + "> dct:hasPart ?assertion . \n");
		sb.append("  ?assertion earl:test ?test . \n");
		sb.append("  ?test dc:title ?testTitle . \n");
		sb.append("  ?assertion earl:result ?result . \n");
		sb.append("  ?result  earl:outcome ?outcome . \n");
		sb.append("  ?outcome dc:title ?outcomeLabel . \n");
		sb.append("  ?assertion earl:subject ?subject . \n");
		sb.append("  ?subject dc:title ?subjectTitle . \n");
		sb.append("} \n");
		sb.append("ORDER BY ?subjectTitle ?testTitle \n");
    	return sb.toString();
    }
	
	public static String buildGetTestHttpTraces(String test) {
		StringBuilder sb = new StringBuilder();
		sb.append("PREFIX earl: <http://www.w3.org/ns/earl#> \n");
		sb.append("PREFIX dct: <http://purl.org/dc/terms/> \n");
		sb.append("PREFIX http: <http://www.w3.org/2006/http#> \n");
		sb.append("PREFIX vapour: <http://vapour.sourceforge.net/vocab.rdf#> \n");
		sb.append("SELECT ?response ?responseTitle ?absoluteUri ?statusCodeNumber ?responseContentType ?responseLocation \n");
		sb.append("       ?statusCodeTest ?statusCodeValidity ?responseContentTypeTest ?responseContentTypeValidity \n");
		sb.append("       ?requestAccept ?previousRequestCount ?requestType ?requestMethodName ?requestAbsPath \n");
		sb.append("       ?requestHost ?responseVary ?userAgent ?assertion \n");
		sb.append("WHERE { \n");
		sb.append("     <" + test + "> dct:hasPart ?assertion . \n");
		sb.append("     ?assertion earl:subject ?response . \n");
		sb.append("     ?response a earl:TestSubject ; \n");
		sb.append("       dc:title ?responseTitle ; \n");
		sb.append("       http:statusCodeNumber ?statusCodeNumber ; \n");
		sb.append("       vapour:previousRequestCount ?previousRequestCount . \n");
		sb.append("     ?request http:response ?response ; \n");
		sb.append("       http:absoluteURI ?absoluteUri ; \n");
		sb.append("       http:methodName ?requestMethodName ; \n");
		sb.append("       http:abs_path ?requestAbsPath ; \n");
		sb.append("       http:host ?requestHost . \n");
		sb.append("     OPTIONAL { ?request http:accept ?requestAccept . } \n");
		sb.append("     OPTIONAL { ?request http:user-agent ?userAgent . } \n");
		sb.append("     OPTIONAL { ?response http:content-type ?responseContentType . } \n");
		sb.append("     OPTIONAL { ?response http:location ?responseLocation . } \n");
		sb.append("     OPTIONAL { ?response http:vary ?responseVary . } \n");
		sb.append("     OPTIONAL { \n");
		sb.append("                 ?statusCodeAssertion earl:subject ?response . \n");
		sb.append("                 ?statusCodeAssertion earl:test ?statusCodeTest . \n");
		sb.append("                 ?statusCodeTest earl:propertyUnderTest http:statusCodeNumber . \n");
		sb.append("                 ?statusCodeAssertion earl:result ?statusCodeResult . \n");
		sb.append("                 ?statusCodeResult earl:outcome ?statusCodeValidity . \n");
		sb.append("     } \n");
		sb.append("     OPTIONAL { \n");
		sb.append("                 ?responseContentTypeAssertion earl:subject ?response . \n");
		sb.append("                 ?responseContentTypeAssertion earl:test ?responseContentTypeTest . \n");
		sb.append("                 ?responseContentTypeTest vapour:propertyUnderTest http:content-type . \n");
		sb.append("                 ?responseContentTypeAssertion earl:result ?responseContentTypeResult . \n");
		sb.append("                 ?responseContentTypeResult earl:outcome ?responseContentTypeValidity . \n");
		sb.append("     } \n");
		sb.append("} \n");
		sb.append("ORDER BY ?previousRequestCount \n");
		return sb.toString();
	}
	
}
