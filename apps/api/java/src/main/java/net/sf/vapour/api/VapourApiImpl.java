package net.sf.vapour.api;

import java.io.IOException;
import java.io.StringReader;
import java.util.ArrayList;
import java.util.List;


import org.apache.http.HttpEntity;
import org.apache.http.HttpResponse;
import org.apache.http.NameValuePair;
import org.apache.http.client.ClientProtocolException;
import org.apache.http.client.HttpClient;
import org.apache.http.client.methods.HttpGet;
import org.apache.http.client.utils.URLEncodedUtils;
import org.apache.http.impl.client.DefaultHttpClient;
import org.apache.http.message.BasicNameValuePair;
import org.apache.http.util.EntityUtils;
import org.apache.log4j.Logger;

import com.hp.hpl.jena.rdf.model.Model;
import com.hp.hpl.jena.rdf.model.ModelFactory;

class VapourApiImpl implements VapourApi {

	private static final Logger log = Logger.getLogger(VapourApiImpl.class);
	private static final String VAPOUR_CACHE_PATH = "vapour.cache";
	public static final String URI_PARAM = "vocabUri"; //FIXME: change to 'uri' on the new versions
	public static final String VALIDATE_RDF_PARAM = "validateRDF";
	public static final String HTML_VERSION_PARAM = "htmlVersions";
	public static final String DEFAULT_RESPONSE_PARAM = "defaultResponse";
	public static final String USER_AGENT_PARAM = "userAgent";
	public static final String FORMAT_PARAM = "format";
	private boolean cache;
	private String service;

	public VapourApiImpl(String service) {
		super();
		this.cache = false;
		this.service = service;
		log.info("Create API against " + this.service);
	}

	public VapourReport check(String uri) {
		return this.check(uri, false, false, Format.RDFXML, "vapour.sourceforge.net");
	}
	
	public void enableCacheDump() {
		this.cache = true;
	}

	public VapourReport check(String uri, boolean meaningful, boolean html, Format format) {
		return this.check(uri, meaningful, html, format, "vapour.sourceforge.net");
	}
	
	private VapourReport check(String uri, boolean meaningful, boolean html, Format format, String useragent) {
		log.debug("Checking '" + uri + "'...");
		HttpClient client = new DefaultHttpClient();
		List<NameValuePair> params = new ArrayList<NameValuePair>();
		params.add(new BasicNameValuePair(URI_PARAM, uri));
		params.add(new BasicNameValuePair(VALIDATE_RDF_PARAM, (meaningful ? "1" : "0")));
		params.add(new BasicNameValuePair(HTML_VERSION_PARAM, (html ? "1" : "0")));
		params.add(new BasicNameValuePair(DEFAULT_RESPONSE_PARAM, format.name().toLowerCase()));
		params.add(new BasicNameValuePair(USER_AGENT_PARAM, useragent));
		params.add(new BasicNameValuePair(FORMAT_PARAM, "rdf"));
		HttpGet method = new HttpGet(this.service + "?" + URLEncodedUtils.format(params, "utf-8"));
		method.setHeader("Accept", "application/rdf+xml"); 
		method.setHeader("User-Agent", "Vapour API/1.0"); 
		
		log.debug("Performing check using the query: " + method.getURI().getQuery());
		try {
			HttpResponse response = client.execute(method);   
	    	HttpEntity entity = response.getEntity();
	    	String content = EntityUtils.toString(entity);
			StringReader reader = new StringReader(content);
			log.trace("RAW Content: " + content);
	    	Model model = ModelFactory.createDefaultModel();
	    	model.read(reader, this.service);
	    	VapourReportImpl report = new VapourReportImpl(model);
	    	if (this.cache) { 
	    		FileHelper.writeModel(model, VAPOUR_CACHE_PATH);
	    		log.info("Written " + model.size() + " statements as cache");
	    	}
			return report;
		} catch (ClientProtocolException e) {
			log.error(e);
			throw new RuntimeException(e);
		} catch (IOException e) {
			log.error(e);
			throw new RuntimeException(e);
		}
	}

}
