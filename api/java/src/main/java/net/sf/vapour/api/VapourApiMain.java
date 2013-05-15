package net.sf.vapour.api;

import java.io.IOException;
import java.io.OutputStream;
import java.io.PrintWriter;
import java.nio.charset.Charset;

import org.apache.commons.cli.CommandLine;
import org.apache.commons.cli.CommandLineParser;
import org.apache.commons.cli.HelpFormatter;
import org.apache.commons.cli.Option;
import org.apache.commons.cli.Options;
import org.apache.commons.cli.ParseException;
import org.apache.commons.cli.PosixParser;

public class VapourApiMain {
	
	public static void main(String[] args) throws IOException {
		final Option helpOption = new Option("h", "help", false, "Option for printing");
		final Option uriOption = new Option("u", "uri", true, "URI to check");
		uriOption.setRequired(true);
		final Option testOption = new Option("t", "tests", false, "Show tests details");
		final Option cacheOption = new Option("c", "cache", false, "Dumps on disk the test suite cache");
		final Options options = new Options();
		options.addOption(helpOption).addOption(uriOption).addOption(testOption).addOption(cacheOption);
		try {
			final CommandLineParser cmdLinePosixParser = new PosixParser();
			CommandLine cmd = cmdLinePosixParser.parse(options, args);
			if (cmd.hasOption("help")) {
				printHelp(options, System.out);
			}
			String uri = cmd.getOptionValue("uri");
			VapourApi api = VapourApiFactory.createVapourApi();
			if (cmd.hasOption("c")) {
				api.enableCacheDump();
			}
			VapourReport report = api.check(uri);
			System.out.println();
			System.out.println("Vapour Report:");
			System.out.println("-------------");
			System.out.println("URI: " + uri + "");
			System.out.println("Result: " + report + "");
			System.out.println();
			if (cmd.hasOption("t")) {
				System.out.println("Tests:");
				for (VapourTest test : report.getTests()) {
					System.out.println(test);
				}
				System.out.println();
			}
		} catch (ParseException e) {
			System.err.println("Encountered exception while parsing options: " + e.getMessage());
			printHelp(options, System.out);
		}
	}	
	
	public static void printHelp(final Options options, final OutputStream out) throws IOException {
		out.write("\n".getBytes(Charset.forName("UTF-8")));
		final String commandLineSyntax = "java -jar vapour-api.jar";
		final PrintWriter writer = new PrintWriter(out);
		final HelpFormatter helpFormatter = new HelpFormatter();
		helpFormatter.printHelp(writer, 80, commandLineSyntax, "\nHelp:", options, 3, 5, "", true);
		writer.flush();
		out.write("\n".getBytes(Charset.forName("UTF-8")));
	}

}
