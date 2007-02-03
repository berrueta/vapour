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

public class Recipe1aTest extends AbstractTestCase {
	
    private static final String BASE_URI = PURL_BASE_URI + "example6";
    private static final String RDF_BASE_URI = COMMON_BASE_URI + "example6.rdf";

	public void testVocabularyDefault() throws Exception {
    	WebResponse resp = executeRequest(BASE_URI);
    	assertResponseCode302(resp);
    	assertEquals(RDF_BASE_URI, getLocation(resp));
    	WebResponse resp2 = followRedirect(resp);
    	assertResponseCode200(resp2);
    	assertContentTypeRdfXml(resp2);
    }
    
    public void testClassDefinitionDefault() throws Exception {
    	WebResponse resp = executeRequest(BASE_URI + "#ClassA");
    	assertResponseCode302(resp);
    	assertEquals(RDF_BASE_URI, getLocation(resp));
    	WebResponse resp2 = followRedirect(resp);
    	assertResponseCode200(resp2);
    	assertContentTypeRdfXml(resp2);
    }
    
    public void testPropertyDefinitionDefault() throws Exception {
    	WebResponse resp = executeRequest(BASE_URI + "#propA");
    	assertResponseCode302(resp);
    	assertEquals(RDF_BASE_URI, getLocation(resp));
    	WebResponse resp2 = followRedirect(resp);
    	assertResponseCode200(resp2);
    	assertContentTypeRdfXml(resp2);
    }
	
}
