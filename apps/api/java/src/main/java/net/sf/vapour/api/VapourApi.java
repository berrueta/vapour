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
	
	VapourReport check(String uri);
	
	VapourReport check(String uri, boolean meaningful, boolean html, Format format);

	void enableCacheDump();

}
