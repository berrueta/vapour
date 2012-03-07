package net.sf.vapour.api;

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
