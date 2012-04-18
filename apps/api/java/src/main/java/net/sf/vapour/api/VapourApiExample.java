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
 * Dummy example of the API usage
 * 
 * @author sergio.fernandez@fundacionctic.org
 *
 */
public class VapourApiExample {

	public static void main(String[] args) {
		String uri = "http://dbpedia.org/resource/Asturias";
		VapourApi api = VapourApiFactory.createVapourApi();
		//VapourApi api = VapourApiFactory.createVapourApi("http://localhost:8000/vapour");
		api.enableCacheDump();
		VapourReport report = api.check(uri);
		System.out.println();
		System.out.println("Vapour Report:");
		System.out.println("-------------");
		System.out.println("URI: " + uri + "");
		System.out.println("Result: " + report + "");
		System.out.println();
		System.out.println("Tests:");
		for (VapourTest test : report.getTests()) {
			System.out.println(test);
		}
	}

}
