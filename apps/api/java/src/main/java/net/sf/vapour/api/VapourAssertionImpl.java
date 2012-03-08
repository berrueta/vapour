package net.sf.vapour.api;

import com.hp.hpl.jena.query.QuerySolution;

class VapourAssertionImpl implements VapourAssertion {
	
	String id;
	VapourRequest request;
	VapourResponse response;

	public VapourAssertionImpl(QuerySolution qs) {
		this.id = qs.get("assertion").toString();
		this.buildRequest(qs);
		this.buildResponse(qs);
	}

	private void buildRequest(QuerySolution qs) {
		String method = qs.getLiteral("requestMethodName").getString();
		String uri = qs.getLiteral("absoluteUri").getString();
		String acceptHeader = (qs.getLiteral("requestAccept") != null ? qs.getLiteral("requestAccept").getString() : null);
		String userAgent = qs.getLiteral("userAgent").getString();
		this.request = new VapourRequestImpl(method, uri, acceptHeader, userAgent);
	}

	private void buildResponse(QuerySolution qs) {
		String title = qs.getLiteral("responseTitle").getString();
		int statusCode = qs.getLiteral("statusCodeNumber").getInt();
		String location = (qs.getLiteral("responseLocation") != null ? qs.getLiteral("responseLocation").getString() : null);
		String contentType = qs.getLiteral("responseContentType").getString();
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
		return (o.getResponse().getPreviousRequestCount() - this.getResponse().getPreviousRequestCount());
	}

	@Override
	public int hashCode() {
		final int prime = 31;
		int result = 1;
		result = prime * result + ((id == null) ? 0 : id.hashCode());
		return result;
	}

	@Override
	public boolean equals(Object obj) {
		if (this == obj)
			return true;
		if (obj == null)
			return false;
		if (getClass() != obj.getClass())
			return false;
		VapourAssertionImpl other = (VapourAssertionImpl) obj;
		if (id == null) {
			if (other.id != null)
				return false;
		} else if (!id.equals(other.id))
			return false;
		return true;
	}

	@Override
	public String toString() {
		return "Vapour Assertion '" + id + "':\n " + request + "\n" + response + "\n";
	}

}
