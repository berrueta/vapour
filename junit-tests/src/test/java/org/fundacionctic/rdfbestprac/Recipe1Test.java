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

public class Recipe1Test extends AbstractTestCase
{

    private static final String BASE_URI = COMMON_BASE_URI + "example1";

	public void testVocabularyDefault() throws Exception {
    	WebResponse resp = executeRequest(BASE_URI);
    	assertResponseCode200(resp);
    	assertContentTypeRdfXml(resp);
    }
    
    public void testClassDefinitionDefault() throws Exception {
    	WebResponse resp = executeRequest(BASE_URI + "#ClassA");
    	assertResponseCode200(resp);
    	assertContentTypeRdfXml(resp);    	
    }
    
    public void testPropertyDefinitionDefault() throws Exception {
    	WebResponse resp = executeRequest(BASE_URI + "#propA");
    	assertResponseCode200(resp);
    	assertContentTypeRdfXml(resp);
    }
	
}
