package net.sf.vapour.api;

public interface VapourResponse {
	
	int getStatusCode();
	
	String getLocation();
	
	String getContentType();
	
	String getBody();

}
