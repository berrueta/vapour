package net.sf.vapour.api.helpers;

import java.io.BufferedWriter;
import java.io.FileWriter;
import java.io.IOException;

import org.apache.log4j.Logger;

import com.hp.hpl.jena.rdf.model.Model;

public class FileHelper {
	
	private static final Logger log = Logger.getLogger(FileHelper.class);
	private static final String RDF_SERALIZATION = "RDF/XML-ABBREV";
	
	public static void writeModel(Model model, String path) {
		try {		
			log.debug("Writing " + model.size() + "  statements as cache...");
			FileWriter fw = new FileWriter(path);
			BufferedWriter out = new BufferedWriter(fw);
			model.write(out, RDF_SERALIZATION);
		} catch (IOException e) {
			log.error("Error writing '" + path + "': " + e.getMessage());
		}
	}

}
