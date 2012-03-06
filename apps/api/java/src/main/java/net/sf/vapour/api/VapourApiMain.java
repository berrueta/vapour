package net.sf.vapour.api;

public class VapourApiMain {

	public static void main(String[] args) {
		String uri = "http://dbpedia.org/resource/Asturias";
		VapourApi api = VapourApiFactory.createVapourApi();
		api.enableCacheDump();
		VapourReport report = api.check(uri);
		System.out.println();
		System.out.println("Vapour Report:");
		System.out.println("-------------");
		System.out.println("URI: " + uri + "");
		System.out.println("Result: " + report + "");
		System.out.println("Tests performed: " + report.getTestPerformed());
		System.out.println("Tests passed: " + report.getTestPassed());
		System.out.println("Tests failed: " + report.getTestFailed());
	}

}
