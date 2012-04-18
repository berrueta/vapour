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
 * Factory methods for creation of APIs against Vapour
 * 
 * @author sergio.fernandez@fundacionctic.org
 *
 */
public class VapourApiFactory {
	
	private static final String PUBLIC_SERVICE = "http://validator.linkeddata.org/vapour";

	/**
	 * Create a Vapour API instance against the public service 
	 * (http://validator.linkeddata.org/vapour)
	 * 
	 * @return Vapour API instance
	 */
	public static VapourApi createVapourApi() {
		return new VapourApiImpl(PUBLIC_SERVICE);
	}
	
	/**
	 * Create a Vapour API instance against a custom service 
	 * (commonly for testing purposes)
	 * 
	 * @return Vapour API instance
	 */	
	public static VapourApi createVapourApi(String service) {
		return new VapourApiImpl(service);
	}

}
