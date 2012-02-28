package net.sf.vapour.api;

import java.util.List;

public interface VapourReport {
	
	int getTestPerformed();
	
	int getTestPassed();
	
	List<VapourTest> getTests();

}
