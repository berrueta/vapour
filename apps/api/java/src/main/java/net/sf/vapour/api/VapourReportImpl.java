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

import java.util.Collections;
import java.util.LinkedList;
import java.util.List;

import org.apache.log4j.Logger;

import com.hp.hpl.jena.query.QuerySolution;
import com.hp.hpl.jena.query.ResultSet;
import com.hp.hpl.jena.rdf.model.Model;

/**
 * Implementation of a Vapour report
 * 
 * @author sergio.fernandez@fundacionctic.org
 *
 */
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

	public int getPerformedTests() {
		return SparqlHelper.execCountQuery(this.model, QueryBuilder.buildCountTests());
	}

	public int getPassedTests() {
		return (this.getPerformedTests() - this.getFailedTests()); //FIXME: find a query for query for getting such result directly
	}
	 
	public int getFailedTests() {
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
		return (this.isValid() ? "all tests passed" : "some tests failed") + " (" + this.getPassedTests() + " passed/" + this.getPerformedTests() + " total)";
	}
	
}
