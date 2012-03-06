package net.sf.vapour.api;

import java.util.LinkedList;
import java.util.List;

import org.apache.log4j.Logger;

import com.hp.hpl.jena.query.QuerySolution;
import com.hp.hpl.jena.query.ResultSet;
import com.hp.hpl.jena.rdf.model.Model;

class VapourReportImpl implements VapourReport {
	
	private static final Logger log = Logger.getLogger(VapourReportImpl.class);
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
		return SparqlHelper.execCountQuery(this.model, QueryBuilder.buildCountPassedTests());
	}
	 
	public int getTestFailed() {
		return SparqlHelper.execCountQuery(this.model, QueryBuilder.buildCountFailedTests());
	}

	public List<VapourTest> getTests() {
		List<VapourTest> tests = new LinkedList<VapourTest>();
		ResultSet results = SparqlHelper.execSelectQuery(this.model, QueryBuilder.buildGetTests());
		while(results.hasNext()) {
			QuerySolution result = results.nextSolution();
			VapourTest test = new VapourTestImpl(result, this.model);
			tests.add(test);
		}
		return tests;
	}

	@Override
	public String toString() {
		return (this.isValid() ? "all tests passed" : "some tests failed") + " (" + this.getTestPassed() + "/" + this.getTestPerformed() + ")";
	}
	
}
