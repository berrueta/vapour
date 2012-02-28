package net.sf.vapour.api;

public interface VapourRequest {
	
	String getUrl();
	
	String getMethod();
	
	String getAcceptHeader();
	
	String getUserAgent();

}
