package net.sf.vapour.api;

import java.util.List;

public interface VapourReport {
	
	boolean isValid();
	
	int getTestPerformed();
	
	int getTestPassed();
	
	int getTestFailed();
	
	List<VapourTest> getTests();

}
