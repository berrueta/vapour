/**
 * Copyright (C) 2012 Fundación CTIC <http://fundacionctic.org>, All Rights Reserved.
 *
 * This work is distributed under the W3C® Software License in the hope that it will be
 * useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY
 * or FITNESS FOR A PARTICULAR PURPOSE.
 *
 * You may obtain a copy of the License at
 *
 *     http://www.w3.org/Consortium/Legal/2002/copyright-software-20021231
 */
package net.sf.vapour.api;

import org.apache.log4j.Logger;

import com.hp.hpl.jena.query.QueryExecution;
import com.hp.hpl.jena.query.QueryExecutionFactory;
import com.hp.hpl.jena.query.QueryFactory;
import com.hp.hpl.jena.query.ResultSet;
import com.hp.hpl.jena.rdf.model.Model;

/**
 * Helper for working with SPARQL using Apache Jena
 * 
 * @author sergio.fernandez@fundacionctic.org
 *
 */
class SparqlHelper {
	
	private static final Logger log = Logger.getLogger(SparqlHelper.class);
	
	public static int execCountQuery(Model model, String query) {
		return execCountQuery(model, query, "count");
	}
	
	public static int execCountQuery(Model model, String query, String var) {
		log.trace("Query: " + query);
		QueryExecution qe = QueryExecutionFactory.create(QueryFactory.create(query), model);
		ResultSet results = qe.execSelect();
		int countResult = results.nextSolution().getLiteral(var).getInt();
		log.trace("COUNT query result: " + countResult);
		return countResult;
	}

	public static boolean execAskQuery(Model model, String query) {
		log.trace("Query: " + query);
		QueryExecution qe = QueryExecutionFactory.create(QueryFactory.create(query), model);
		boolean askResult = qe.execAsk();
		log.trace("ASK query result: " + askResult);
		return askResult;
	}
	
	public static ResultSet execSelectQuery(Model model, String query) {
		log.trace("Query: " + query);
		QueryExecution qe = QueryExecutionFactory.create(QueryFactory.create(query), model);
		return qe.execSelect();
	}

	public static Model execDescribeQuery(Model model, String query) {
		log.trace("Query: " + query);
		QueryExecution qe = QueryExecutionFactory.create(QueryFactory.create(query), model);
		return qe.execDescribe();
	}

}
