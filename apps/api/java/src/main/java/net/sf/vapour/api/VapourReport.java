package net.sf.vapour.api;

import java.util.List;

/**
 * Definition of a Vapour report
 * 
 * @author sergio.fernandez@fundacionctic.org
 *
 */
public interface VapourReport {
	
	boolean isValid();
	
	int getTestPerformed();
	
	int getTestPassed();
	
	int getTestFailed();
	
	List<VapourTest> getTests();

}
