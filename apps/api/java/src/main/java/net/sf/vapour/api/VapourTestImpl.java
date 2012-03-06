package net.sf.vapour.api;

import com.hp.hpl.jena.query.QuerySolution;
import com.hp.hpl.jena.rdf.model.Model;

class VapourTestImpl implements VapourTest, Comparable<VapourTest> {
	
	private String id;
	private String title;
	private int order;
	private boolean success;
	private String url;
	private String ct;
	private VapourTrace trace;
	private Model model;
	
	public VapourTestImpl() {
		super();
		this.trace = null;
	}

	public VapourTestImpl(QuerySolution result, Model model) {
		this();
		this.id = result.getResource("testRequirement").getURI();
		this.title = result.getLiteral("testRequirementTitle").getString();
		this.order = result.getLiteral("testRequirementOrder").getInt();
		this.model = SparqlHelper.execDescribeQuery(model, QueryBuilder.buildDescribe(this.id));
		this.success = SparqlHelper.execAskQuery(this.model, QueryBuilder.buildAskFailedTest(this.id));
		QuerySolution finalUri = SparqlHelper.execSelectQuery(this.model, QueryBuilder.buildGetTestFinalUri(this.id)).nextSolution();
		this.url = finalUri.getResource("finalUri").getURI();
		this.ct = finalUri.getLiteral("contentType").getString();
	}
	
	public String getId() {
		return this.id;
	}

	public String getTitle() {
		return this.title;
	}

	public int getOrder() {
		return this.order;
	}

	public boolean getSucess() {
		return this.success;
	}
	
	public String getFinalUri() {
		return this.url;
	}
	
	public String getFinalContentType() {
		return this.ct;
	}

	public VapourTrace getTrace() {
		if (this.trace == null) {
			throw new RuntimeException("unimplemented");
		}
		return this.trace;
	}

	public int compareTo(VapourTest o) {
		return this.order - o.getOrder();
	}

	@Override
	public int hashCode() {
		final int prime = 31;
		int result = 1;
		result = prime * result + ((id == null) ? 0 : id.hashCode());
		result = prime * result + order;
		result = prime * result + ((title == null) ? 0 : title.hashCode());
		return result;
	}

	@Override
	public boolean equals(Object obj) {
		if (this == obj)
			return true;
		if (obj == null)
			return false;
		if (getClass() != obj.getClass())
			return false;
		VapourTestImpl other = (VapourTestImpl) obj;
		if (id == null) {
			if (other.id != null)
				return false;
		} else if (!id.equals(other.id))
			return false;
		if (order != other.order)
			return false;
		if (title == null) {
			if (other.title != null)
				return false;
		} else if (!title.equals(other.title))
			return false;
		return true;
	}
	
}
