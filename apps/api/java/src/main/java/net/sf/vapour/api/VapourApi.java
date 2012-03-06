package net.sf.vapour.api;

public interface VapourApi {
	
	VapourReport check(String uri);
	
	VapourReport check(String uri, boolean meaningful, boolean html, Format format);

	void enableCacheDump();

}
