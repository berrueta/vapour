package net.sf.vapour.api;

public interface VapourTest {
	
	String getId();
	
	String getTitle();
	
	int getOrder();
	
	boolean getSucess();
	
	String getFinalUri();
	
	String getFinalContentType();
	
	VapourTrace getTrace();

}
