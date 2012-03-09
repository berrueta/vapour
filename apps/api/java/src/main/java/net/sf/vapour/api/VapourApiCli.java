package net.sf.vapour.api;

import java.io.OutputStream;
import java.io.PrintWriter;

import org.apache.commons.cli.CommandLine;
import org.apache.commons.cli.CommandLineParser;
import org.apache.commons.cli.HelpFormatter;
import org.apache.commons.cli.Option;
import org.apache.commons.cli.Options;
import org.apache.commons.cli.ParseException;
import org.apache.commons.cli.PosixParser;

public class VapourApiCli {

	public static void main(String[] args) {
		
		final Option option = new Option("u", "uri", true, "URI to check");
		option.setRequired(true);
		final Options options = new Options();
		options.addOption("h", "help", false, "Option for printing help")
				.addOption("s", "service", true, "Vapour service to access its API, by default the public web service at validator.linkeddata.org")
				.addOption(option);
		try {
			final CommandLineParser cmdLinePosixParser = new PosixParser();
			CommandLine commandLine = cmdLinePosixParser.parse(options, args);
			if (commandLine.hasOption("help")) {
				printHelp(options, System.out);
			}

			VapourApi api;
			
			if (commandLine.hasOption("service")) {
				api = VapourApiFactory.createVapourApi(commandLine.getOptionValue("service"));
			} else {
				api = VapourApiFactory.createVapourApi();
			}

			String uri = commandLine.getOptionValue("uri");
			api.check(uri);
			
		} catch (ParseException parseException) {
			System.err.println("Encountered exception while parsing options:\n"
				+ parseException.getMessage());
		}
	}

	public static void printHelp(final Options options, final OutputStream out) {
		final String commandLineSyntax = "mvn exec:java -Dexec.mainClass=\"net.sf.vapour.api.VapourApiCli\"";
		final PrintWriter writer = new PrintWriter(out);
		final HelpFormatter helpFormatter = new HelpFormatter();
		helpFormatter.printHelp(writer, 80, commandLineSyntax, "HELP", options, 3, 5, "", true);
		writer.flush();
		System.exit(0);
	}

}
