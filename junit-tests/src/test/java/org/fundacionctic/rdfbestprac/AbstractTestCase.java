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

import org.apache.log4j.Logger;

import com.meterware.httpunit.GetMethodWebRequest;
import com.meterware.httpunit.WebConversation;
import com.meterware.httpunit.WebRequest;
import com.meterware.httpunit.WebResponse;

import junit.framework.TestCase;

public abstract class AbstractTestCase extends TestCase {

	private static final String HTTP_HEADER_LOCATION = "Location";
	private static final String HTTP_HEADER_ACCEPT = "Accept";
	
	private static final String MIME_TYPE_APPLICATION_RDF_XML = "application/rdf+xml";
	private static final String MIME_TYPE_TEXT_HTML = "text/html";

	protected static final String ACCEPT_HTML = MIME_TYPE_TEXT_HTML;
	protected static final String ACCEPT_RDF_XML = MIME_TYPE_APPLICATION_RDF_XML;
	
	private static final Logger logger = Logger.getLogger(AbstractTestCase.class);
	
    //protected static final String COMMON_BASE_URI = "http://isegserv.itd.rl.ac.uk/VM/http-examples/";
    protected static final String COMMON_BASE_URI = "http://vapour.sourceforge.net/recipes-web/";
	//protected static final String COMMON_BASE_URI = "http://localhost/~berrueta/recipes/";
	protected static final String PURL_BASE_URI = "http://purl.org/net/swbp-vm/";

	protected WebResponse executeRequest(String uri, String accept) throws Exception {
		WebRequest req = new GetMethodWebRequest(uri);
		if (accept != null) {
			req.setHeaderField(HTTP_HEADER_ACCEPT, accept);
		} else {
			req.setHeaderField(HTTP_HEADER_ACCEPT, "");
		}
    	WebConversation wc = new WebConversation();
    	wc.getClientProperties().setAutoRedirect(false);
    	logger.debug("Requesting: " + uri);
    	WebResponse resp = wc.getResponse(req);
		return resp;
	}
	
	protected WebResponse executeRequest(String uri) throws Exception {
		return executeRequest(uri, null);
	}

	protected WebResponse followRedirect(WebResponse resp) throws Exception {
		return executeRequest(getLocation(resp));
	}

	protected WebResponse followRedirect(WebResponse resp, String accept) throws Exception {
		return executeRequest(getLocation(resp), accept);
	}

	protected void assertResponseCode200(WebResponse resp) {
		assertEquals(200, resp.getResponseCode());
	}
	
	protected void assertResponseCode302(WebResponse resp) {
		assertEquals(302, resp.getResponseCode());
	}

	protected void assertResponseCode303(WebResponse resp) {
		assertEquals(303, resp.getResponseCode());
	}

	protected void assertContentTypeHtml(WebResponse resp) {
		assertEquals(MIME_TYPE_TEXT_HTML, resp.getContentType());
	}

	protected void assertContentTypeRdfXml(WebResponse resp) {
		assertEquals(MIME_TYPE_APPLICATION_RDF_XML, resp.getContentType());
	}

	protected String getLocation(WebResponse resp) {
		return resp.getHeaderField(HTTP_HEADER_LOCATION);
	}
    
}
