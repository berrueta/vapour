package net.sf.vapour.api;

import java.util.List;

public interface VapourTest {
	
	String getId();
	
	String getTitle();
	
	int getOrder();
	
	boolean getSucess();
	
	String getFinalUri();
	
	String getFinalContentType();
	
	List<VapourAssertion> getAssertions();

}
