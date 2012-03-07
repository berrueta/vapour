package net.sf.vapour.api;

public interface VapourAssertion extends Comparable<VapourAssertion> {
	
	VapourRequest getRequest();
	
	VapourResponse getResponse();

}
