package net.sf.vapour.api;

import java.util.List;

/**
 * Definition of a test in Vapour
 * 
 * @author sergio.fernandez@fundacionctic.org
 *
 */
public interface VapourTest extends Comparable<VapourTest> {
	
	String getId();
	
	String getTitle();
	
	int getOrder();
	
	boolean getSucess();
	
	String getFinalUri();
	
	String getFinalContentType();
	
	List<VapourAssertion> getAssertions();

}
