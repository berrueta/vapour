package net.sf.vapour.api;

class QueryBuilder {
	
	public static String buildTestsCount() {
		StringBuilder sb = new StringBuilder();
		sb.append("PREFIX earl: <http://www.w3.org/ns/earl#> \n");
		sb.append("SELECT (count(?assertion) as ?count) \n");
		sb.append("WHERE { \n");
		sb.append("  ?assertion a earl:Assertion . \n");
		sb.append("}");
		return sb.toString();
	}
	
	public static String buildPassedTestsCount() {
		StringBuilder sb = new StringBuilder();
		sb.append("PREFIX earl: <http://www.w3.org/ns/earl#> \n");
		sb.append("SELECT (count(?assertion) as ?count) \n");
		sb.append("WHERE { \n");
		sb.append("  ?assertion a earl:Assertion . \n");
        sb.append("  ?assertion earl:result ?result . \n");
        sb.append("  ?result earl:outcome earl:passed . \n");
		sb.append("}");
		return sb.toString();
	}
	
	public static String buildFailedTestsCount() {
		StringBuilder sb = new StringBuilder();
		sb.append("PREFIX earl: <http://www.w3.org/ns/earl#> \n");
		sb.append("SELECT (count(?assertion) as ?count) \n");
		sb.append("WHERE { \n");
		sb.append("  ?assertion a earl:Assertion . \n");
        sb.append("  ?assertion earl:result ?result . \n");
        sb.append("  ?result earl:outcome earl:failed . \n");
		sb.append("}");
		return sb.toString();
	}

}
