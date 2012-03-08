package net.sf.vapour.api;

/**
 * Definition of a request in Vapour 
 * 
 * @author sergio.fernandez@fundacionctic.org
 *
 */
public interface VapourRequest {
	
	String getUri();
	
	String getMethod();
	
	String getAcceptHeader();
	
	String getUserAgent();

}
