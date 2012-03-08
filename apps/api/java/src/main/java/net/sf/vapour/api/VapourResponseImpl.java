package net.sf.vapour.api;

/**
 * Implementation of a response in Vapour
 * 
 * @author sergio.fernandez@fundacionctic.org
 *
 */
class VapourResponseImpl implements VapourResponse {
	
	private String title;
	private int statusCode;
	private String location;
	private String contentType;
	private int previousRequestCount;
	
	public VapourResponseImpl() {
		super();
	}

	public VapourResponseImpl(String title, int statusCode, String location, String contentType, int previousRequestCount) {
		this();
		this.title = title;
		this.statusCode = statusCode;
		this.location = location;
		this.contentType = contentType;
		this.previousRequestCount = previousRequestCount;
	}
	
	public String getTitle() {
		return title;
	}

	public int getStatusCode() {
		return this.statusCode;
	}

	public String getLocation() {
		return this.location;
	}

	public String getContentType() {
		return this.contentType;
	}

	public int getPreviousRequestCount() {
		return this.previousRequestCount;
	}

	@Override
	public String toString() {
		return "Vapour Response  [title=" + title + ", statusCode="
				+ statusCode + ", location=" + location + ", contentType="
				+ contentType + ", previousRequestCount="
				+ previousRequestCount + "]";
	}

}
