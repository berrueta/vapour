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
		//VapourApi api = VapourApiFactory.createVapourApi();
		VapourApi api = VapourApiFactory.createVapourApi("http://localhost:8000/vapour");
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
