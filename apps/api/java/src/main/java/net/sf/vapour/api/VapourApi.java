package net.sf.vapour.api;

/**
 * Definition of the Vapour API bindings for Java
 * 
 * @author sergio.fernandez@fundacionctic.org
 *
 */
public interface VapourApi {
	
	VapourReport check(String uri);
	
	VapourReport check(String uri, boolean meaningful, boolean html, Format format);

	void enableCacheDump();

}
