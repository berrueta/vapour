package net.sf.vapour.api;

public interface VapourResponse {
	
	String getTitle();
	
	int getStatusCode();
	
	String getLocation();
	
	String getContentType();
	
	int getPreviousRequestCount();

}
