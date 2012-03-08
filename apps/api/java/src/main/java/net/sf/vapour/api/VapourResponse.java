package net.sf.vapour.api;

/**
 * Definition of a response in Vapour 
 * 
 * @author sergio.fernandez@fundacionctic.org
 *
 */
public interface VapourResponse {
	
	String getTitle();
	
	int getStatusCode();
	
	String getLocation();
	
	String getContentType();
	
	int getPreviousRequestCount();

}
