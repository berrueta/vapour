package net.sf.vapour.api;

public class VapourApiFactory {
	
	/**
	 * Create a Vapour API instance against the public service 
	 * (http://validator.linkeddata.org/vapour)
	 * 
	 * @return Vapour API instance
	 */
	public static VapourApi createVapourApi() {
		return new VapourApiImpl("http://validator.linkeddata.org/vapour");
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
