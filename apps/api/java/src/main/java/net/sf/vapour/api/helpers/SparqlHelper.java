package net.sf.vapour.api.helpers;

import org.apache.log4j.Logger;

import com.hp.hpl.jena.query.QueryExecution;
import com.hp.hpl.jena.query.QueryExecutionFactory;
import com.hp.hpl.jena.query.QueryFactory;
import com.hp.hpl.jena.query.ResultSet;
import com.hp.hpl.jena.rdf.model.Model;

public class SparqlHelper {
	
	private static final Logger log = Logger.getLogger(SparqlHelper.class);
	
	public static int execCountQuery(Model model, String query) {
		return execCountQuery(model, query, "count");
	}
	
	public static int execCountQuery(Model model, String query, String var) {
		log.trace("Query: " + query);
		QueryExecution qe = QueryExecutionFactory.create(QueryFactory.create(query), model);
		ResultSet results = qe.execSelect();
		return results.nextSolution().getLiteral(var).getInt();
	}

	public static boolean execAskQuery(Model model, String query) {
		log.trace("Query: " + query);
		QueryExecution qe = QueryExecutionFactory.create(QueryFactory.create(query), model);
		return qe.execAsk();
	}

}
