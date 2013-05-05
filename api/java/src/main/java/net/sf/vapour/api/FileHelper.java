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
