/**
 * Copyright (C) 2012 Fundación CTIC <http://fundacionctic.org>, All Rights Reserved.
 *
 * This work is distributed under the W3C® Software License in the hope that it will be
 * useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY
 * or FITNESS FOR A PARTICULAR PURPOSE.
 *
 * You may obtain a copy of the License at
 *
 *     http://www.w3.org/Consortium/Legal/2002/copyright-software-20021231
 */
package net.sf.vapour.api;

import com.hp.hpl.jena.query.QuerySolution;

/**
 * Implementation of an asserton in Vapour
 * 
 * @author sergio.fernandez@fundacionctic.org
 *
 */
class VapourAssertionImpl implements VapourAssertion {
	
	VapourRequest request;
	VapourResponse response;

	public VapourAssertionImpl(QuerySolution qs) {
		this.buildRequest(qs);
		this.buildResponse(qs);
	}

	private void buildRequest(QuerySolution qs) {
		String method = qs.get("requestMethodName").toString(); //FIXME: it should be a literal, but comes as a resource
		String uri = qs.getLiteral("absoluteUri").getString();
		String acceptHeader = (qs.getLiteral("requestAccept") != null ? qs.getLiteral("requestAccept").getString() : null);
		String userAgent = qs.getLiteral("userAgent").getString();
		this.request = new VapourRequestImpl(method, uri, acceptHeader, userAgent);
	}

	private void buildResponse(QuerySolution qs) {
		String title = qs.getLiteral("responseTitle").getString();
		int statusCode = qs.getLiteral("statusCodeNumber").getInt();
		String location = (qs.getLiteral("responseLocation") != null ? qs.getLiteral("responseLocation").getString() : null);
		String contentType = (qs.getLiteral("responseContentType") != null ? qs.getLiteral("responseContentType").getString() : null);
		int previousRequestCount = qs.getLiteral("previousRequestCount").getInt();
		this.response = new VapourResponseImpl(title, statusCode, location, contentType, previousRequestCount);
	}

	public VapourRequest getRequest() {
		return this.request;
	}

	public VapourResponse getResponse() {
		return this.response;
	}

	public int compareTo(VapourAssertion o) {
		return (this.getResponse().getPreviousRequestCount() - o.getResponse().getPreviousRequestCount());
	}

	@Override
	public String toString() {
		return "Vapour Assertion:\n " + request + "\n" + response + "\n";
	}

}
