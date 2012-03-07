package net.sf.vapour.api;

import java.util.Collections;
import java.util.LinkedList;
import java.util.List;

import org.apache.log4j.Logger;

import com.hp.hpl.jena.query.QuerySolution;
import com.hp.hpl.jena.query.ResultSet;
import com.hp.hpl.jena.rdf.model.Model;

class VapourReportImpl implements VapourReport {
	
	private static final Logger log = Logger.getLogger(VapourReportImpl.class);
	private List<VapourTest> tests;
	private final Model model;

	public VapourReportImpl(Model model) {
		super();
		this.model = model;
		log.debug("Report created with " + model.size() + " statements");
	}
	
	public boolean isValid() {
		return !SparqlHelper.execAskQuery(this.model, QueryBuilder.buildAskFailedTests());
	}	

	public int getTestPerformed() {
		return SparqlHelper.execCountQuery(this.model, QueryBuilder.buildCountTests());
	}

	public int getTestPassed() {
		return (this.getTestPerformed() - this.getTestFailed()); //FIXME: find a query for query for getting such result directly
	}
	 
	public int getTestFailed() {
		return SparqlHelper.execCountQuery(this.model, QueryBuilder.buildCountFailedTests());
	}

	public List<VapourTest> getTests() {
		if (this.tests == null) {
			this.tests = buildTests();
		}
		return Collections.unmodifiableList(this.tests);
	}

	private List<VapourTest> buildTests() {
		List<VapourTest> tests = new LinkedList<VapourTest>();
		ResultSet results = SparqlHelper.execSelectQuery(this.model, QueryBuilder.buildGetTests());
		while(results.hasNext()) {
			QuerySolution result = results.nextSolution();
			VapourTest test = new VapourTestImpl(result, this.model);
			tests.add(test);
		}
		Collections.sort(tests);
		return tests;
	}

	@Override
	public String toString() {
		return (this.isValid() ? "all tests passed" : "some tests failed") + " (" + this.getTestPassed() + "/" + this.getTestPerformed() + ")";
	}
	
}
