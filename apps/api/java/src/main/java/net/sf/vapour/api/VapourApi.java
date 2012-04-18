/**
 * Copyright (C) 2012 Fundación CTIC <http://fundacionctic.org>, All Rights Reserved.
 *
 * This work is distributed under the W3C® Software License in the hope that it will be
 * useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY
 * or FITNESS FOR A PARTICULAR PURPOSE.
 *
 * You may obtain a copy of the License at
 *
 *     http://www.w3.org/Consortium/Legal/2002/copyright-software-20021231
 */
package net.sf.vapour.api;

/**
 * Definition of the Vapour API bindings for Java
 * 
 * @author sergio.fernandez@fundacionctic.org
 *
 */
public interface VapourApi {
	
	/**
	 * Checks against Vapour is this URI is correctly published according the
	 * Linked Data principles and best practices
	 * 
	 * @param uri uri to test
	 * @return report for the given uri
	 */
	VapourReport check(String uri);
	
	/**
	 * Checks against Vapour is this URI is correctly published according the
	 * Linked Data principles and best practices
	 * 
	 * @param uri uri to tes
	 * @param meaningful check the RDF responses for meaningful data 
	 * @param html check there are HTML descriptions of the symbols
	 * @param format Expected default format for the response
	 * @return report for the given uri
	 */
	VapourReport check(String uri, boolean meaningful, boolean html, Format format);

	/**
	 * Enables to save on disk a RDF cache of the last report
	 * (disabled by default)
	 */
	void enableCacheDump();

}
