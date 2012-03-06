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

	public int getTestPerformed() {
		String query = "PREFIX earl: <http://www.w3.org/ns/earl#> SELECT (count(*) as ?count) WHERE { ?testRequirement a earl:TestRequirement }";
		return SparqlHelper.execCountQuery(this.model, query);
	}

	public int getTestPassed() {
		String query = "PREFIX earl: <http://www.w3.org/ns/earl#> SELECT (count(*) as ?count) WHERE { ?assertion a earl:Assertion . ?assertion earl:result ?result . ?result earl:outcome earl:passed }";
		return SparqlHelper.execCountQuery(this.model, query);
	}
	
	public int getTestFailed() {
		String query = "PREFIX earl: <http://www.w3.org/ns/earl#> SELECT (count(*) as ?count) WHERE { ?assertion a earl:Assertion . ?assertion earl:result ?result . ?result earl:outcome earl:failed }";
		return SparqlHelper.execCountQuery(this.model, query);
	}

	public List<VapourTest> getTests() {
		throw new RuntimeException("Unimplemented");
	}	
	
}
