/*
 *
 * Copyright (c) 2006 - Diego Berrueta (CTIC Foundation)
 *
 * All Rights Reserved. This work is distributed under the W3C Software
 * License in the hope that it will be useful, but WITHOUT ANY WARRANTY;
 * without even the implied warranty of MERCHANTABILITY or FITNESS FOR A
 * PARTICULAR PURPOSE.
 *
 * This work is NOT endorsed by W3C.
 *
 */

package org.fundacionctic.rdfbestprac;

import com.meterware.httpunit.WebResponse;

public class Recipe4Test extends AbstractTestCase {

    private static final String BASE_URI = COMMON_BASE_URI + "example4/";
    private static final String RDF_BASE_URI = COMMON_BASE_URI + "example4-content/2005-10-31.rdf";
    private static final String HTML_BASE_URI = COMMON_BASE_URI + "example4-content/2005-10-31.html";

	public void testVocabularyHTML() throws Exception {
    	WebResponse resp = executeRequest(BASE_URI, ACCEPT_HTML);
    	assertResponseCode303(resp);
    	assertEquals(HTML_BASE_URI, getLocation(resp));
    	WebResponse resp2 = followRedirect(resp, ACCEPT_HTML);
    	assertResponseCode200(resp2);
    	assertContentTypeHtml(resp2);
    }
    
	public void testVocabularyRDF() throws Exception {
    	WebResponse resp = executeRequest(BASE_URI, ACCEPT_RDF_XML);
    	assertResponseCode303(resp);
    	assertEquals(RDF_BASE_URI, getLocation(resp));
    	WebResponse resp2 = followRedirect(resp, ACCEPT_RDF_XML);
    	assertResponseCode200(resp2);
    	assertContentTypeRdfXml(resp2);
    }
    
	public void testVocabularyDefault() throws Exception {
    	WebResponse resp = executeRequest(BASE_URI);
    	assertResponseCode303(resp);
    	assertEquals(RDF_BASE_URI, getLocation(resp));
    	WebResponse resp2 = followRedirect(resp);
    	assertResponseCode200(resp2);
    	assertContentTypeRdfXml(resp2);
    }
    
    public void testClassDefinitionDefault() throws Exception {
    	WebResponse resp = executeRequest(BASE_URI + "/ClassA");
    	assertResponseCode303(resp);
    	assertEquals(RDF_BASE_URI, getLocation(resp));
    	WebResponse resp2 = followRedirect(resp);
    	assertResponseCode200(resp2);
    	assertContentTypeRdfXml(resp2);    	
    }

    public void testClassDefinitionRDF() throws Exception {
    	WebResponse resp = executeRequest(BASE_URI + "/ClassA", ACCEPT_RDF_XML);
    	assertResponseCode303(resp);
    	assertEquals(RDF_BASE_URI, getLocation(resp));
    	WebResponse resp2 = followRedirect(resp);
    	assertResponseCode200(resp2);
    	assertContentTypeRdfXml(resp2);    	
    }

    public void testClassDefinitionHTML() throws Exception {
    	WebResponse resp = executeRequest(BASE_URI + "/ClassA", ACCEPT_HTML);
    	assertResponseCode303(resp);
    	assertEquals(HTML_BASE_URI + "#ClassA", getLocation(resp));
    	WebResponse resp2 = followRedirect(resp);
    	assertResponseCode200(resp2);
    	assertContentTypeHtml(resp2);    	
    }

    public void testPropertyDefinitionDefault() throws Exception {
    	WebResponse resp = executeRequest(BASE_URI + "/propA");
    	assertResponseCode303(resp);
    	assertEquals(RDF_BASE_URI, getLocation(resp));
    	WebResponse resp2 = followRedirect(resp);
    	assertResponseCode200(resp2);
    	assertContentTypeRdfXml(resp2);
    }
	
    public void testPropertyDefinitionRDF() throws Exception {
    	WebResponse resp = executeRequest(BASE_URI + "/propA", ACCEPT_RDF_XML);
    	assertResponseCode303(resp);
    	assertEquals(RDF_BASE_URI, getLocation(resp));
    	WebResponse resp2 = followRedirect(resp);
    	assertResponseCode200(resp2);
    	assertContentTypeRdfXml(resp2);
    }
	
    public void testPropertyDefinitionHTML() throws Exception {
    	WebResponse resp = executeRequest(BASE_URI + "/propA", ACCEPT_HTML);
    	assertResponseCode303(resp);
    	assertEquals(HTML_BASE_URI + "#propA", getLocation(resp));
    	WebResponse resp2 = followRedirect(resp);
    	assertResponseCode200(resp2);
    	assertContentTypeHtml(resp2);
    }
    
}
