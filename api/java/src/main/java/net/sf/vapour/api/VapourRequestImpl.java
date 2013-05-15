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

/**
 * Implementation of a request in Vapour
 * 
 * @author sergio.fernandez@fundacionctic.org
 *
 */
class VapourRequestImpl implements VapourRequest {
	
	private String method;
	private String uri;
	private String acceptHeader;
	private String userAgent;

	public VapourRequestImpl() {
		super();
	}

	public VapourRequestImpl(String method, String uri, String acceptHeader, String userAgent) {
		this();
		this.method = method.toUpperCase();
		this.uri = uri;
		this.acceptHeader = acceptHeader;
		this.userAgent = userAgent;
	}

	public String getMethod() {
		return this.method;
	}
	
	public String getUri() {
		return this.uri;
	}

	public String getAcceptHeader() {
		return this.acceptHeader;
	}

	public String getUserAgent() {
		return this.userAgent;
	}

	@Override
	public String toString() {
		return "Vapour Request [method=" + method + ", uri=" + uri
				+ ", acceptHeader=" + acceptHeader + ", userAgent=" + userAgent
				+ "]";
	}

}
