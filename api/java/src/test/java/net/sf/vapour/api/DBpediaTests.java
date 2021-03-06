package net.sf.vapour.api;

import org.junit.After;
import org.junit.Assert;
import org.junit.Before;
import org.junit.Test;

/**
 * Tests with DBpedia resources
 * 
 * @author sergio.fernandez@fundacionctic.org
 *
 */
public class DBpediaTests {
	
	private static final String URI = "http://dbpedia.org/resource/Asturias";
	private VapourApi api;
	
	@Before
	public void setup() {
		this.api = VapourApiFactory.createVapourApi();
	}
	
	@After
	public void shutdown() {
		this.api = null;
	}
	
	@Test
	public void testDefaultOptions() {
		VapourReport report = this.api.check(URI);
		int tests = report.getPerformedTests();
		int passed = report.getPassedTests();
		int failed = report.getFailedTests();
		Assert.assertEquals(tests, passed + failed);
		Assert.assertEquals(2, tests);
		Assert.assertEquals(2, passed);
		Assert.assertEquals(0, failed);
	}
	
	@Test
	public void testCustomOptions() {
		VapourReport report = this.api.check(URI, true, true, Format.HTML);
		int tests = report.getPerformedTests();
		int passed = report.getPassedTests();
		int failed = report.getFailedTests();
		Assert.assertEquals(tests, passed + failed);
		Assert.assertEquals(3, tests);
		Assert.assertEquals(3, passed);
		Assert.assertEquals(0, failed);
	}
	
	@Test
	public void testCustomOptionsDifferentDefaultFormat() {
		VapourReport report = this.api.check(URI, true, true, Format.RDFXML);
		int tests = report.getPerformedTests();
		int passed = report.getPassedTests();
		int failed = report.getFailedTests();
		Assert.assertEquals(tests, passed + failed);
		Assert.assertEquals(3, tests);
		Assert.assertEquals(3, passed); //FIXME
		Assert.assertEquals(0, failed);
	}
	
}
