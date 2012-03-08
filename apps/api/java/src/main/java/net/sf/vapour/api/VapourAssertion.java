package net.sf.vapour.api;

/**
 * Definition of an assertion in Vapour
 * 
 * @author sergio.fernandez@fundacionctic.org
 *
 */
public interface VapourAssertion extends Comparable<VapourAssertion> {
	
	VapourRequest getRequest();
	
	VapourResponse getResponse();

}
