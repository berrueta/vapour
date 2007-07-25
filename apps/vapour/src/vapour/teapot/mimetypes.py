rdfXml = "application/rdf+xml"
html = "text/html"
xhtml = "application/xhtml+xml"

xhtmlOrHtml = xhtml + "," + html

qualifiedRdfXml = "application/rdf+xml;q=0.5"
qualifiedHtml = "text/html;q=0.5"
qualifiedXhtml = "application/xhtml+xml;q=0.5"

mixed = [ "application/rdf+xml;q=0.5,text/html;q=.3",
 "application/rdf+xml;q=0.3,text/html;q=.5",
 "application/rdf+xml;q=0.5,text/html;q=.5",
 rdfXml + "," + html,
 html + "," + rdfXml ]

requestDescription = {
               rdfXml : "requesting RDF/XML data",
               html : "requesting HTML data",
               xhtml : "requesting XHTML data",
               xhtmlOrHtml : "requesting (X)HTML data",
               qualifiedRdfXml : "requesting RDF/XML with 'q' value",
               qualifiedHtml : "requesting HTML with 'q' value",
               qualifiedXhtml : "requesting XHTML with 'q' value"
               }