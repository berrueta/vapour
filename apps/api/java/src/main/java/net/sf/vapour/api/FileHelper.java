package net.sf.vapour.api;

import java.io.BufferedWriter;
import java.io.FileWriter;
import java.io.IOException;

import org.apache.log4j.Logger;

import com.hp.hpl.jena.rdf.model.Model;

/**
 * Helper for working with files
 * 
 * @author sergio.fernandez@fundacionctic.org
 *
 */
class FileHelper {
	
	private static final Logger log = Logger.getLogger(FileHelper.class);
	private static final String RDF_SERALIZATION = "RDF/XML-ABBREV";
	
	public static void writeModel(Model model, String path) {
		try {		
			FileWriter fw = new FileWriter(path);
			BufferedWriter out = new BufferedWriter(fw);
			model.write(out, RDF_SERALIZATION);
		} catch (IOException e) {
			log.error("Error writing '" + path + "': " + e.getMessage());
		}
	}

}
