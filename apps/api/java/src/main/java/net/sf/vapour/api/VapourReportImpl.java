package net.sf.vapour.api;

import java.util.List;

import net.sf.vapour.api.helpers.SparqlHelper;

import org.apache.log4j.Logger;

import com.hp.hpl.jena.rdf.model.Model;

public class VapourReportImpl implements VapourReport {
	
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
		throw new RuntimeException("Unimplemented");
	}

	@Override
	public String toString() {
		return (this.isValid() ? "all tests passed" : "some tests failed") + " (" + this.getTestPassed() + "/" + this.getTestPerformed() + ")";
	}
	
}
