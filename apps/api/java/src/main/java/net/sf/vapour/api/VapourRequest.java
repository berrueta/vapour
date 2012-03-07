package net.sf.vapour.api;

public interface VapourRequest {
	
	String getUri();
	
	String getMethod();
	
	String getAcceptHeader();
	
	String getUserAgent();

}
