package net.sf.vapour.api;

import java.util.List;

import org.apache.log4j.Logger;

import com.hp.hpl.jena.query.QueryExecution;
import com.hp.hpl.jena.query.QueryExecutionFactory;
import com.hp.hpl.jena.query.QueryFactory;
import com.hp.hpl.jena.query.ResultSet;
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
		return this.execCountQuery(query);
	}

	public int getTestPassed() {
		String query = "PREFIX earl: <http://www.w3.org/ns/earl#> SELECT (count(*) as ?count) WHERE { ?assertion a earl:Assertion . ?assertion earl:result ?result . ?result earl:outcome earl:passed }";
		return this.execCountQuery(query);
	}
	
	public int getTestFailed() {
		String query = "PREFIX earl: <http://www.w3.org/ns/earl#> SELECT (count(*) as ?count) WHERE { ?assertion a earl:Assertion . ?assertion earl:result ?result . ?result earl:outcome earl:failed }";
		return this.execCountQuery(query);
	}

	public List<VapourTest> getTests() {
		throw new RuntimeException("Unimplemented");
	}	
	
	private int execCountQuery(String query) {
		return this.execCountQuery(query, "count");
	}
	
	private int execCountQuery(String query, String var) {
		log.trace("Query: " + query);
		QueryExecution qe = QueryExecutionFactory.create(QueryFactory.create(query), this.model);
		ResultSet results = qe.execSelect();
		return results.nextSolution().getLiteral(var).getInt();
	}

}
