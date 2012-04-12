
rdfXml = "application/rdf+xml"
html = "text/html"
xhtml = "application/xhtml+xml"

xhtmlOrHtml = xhtml + "," + html

mixed = [ "application/rdf+xml;q=0.5,text/html;q=.3",
 "application/rdf+xml;q=0.3,text/html;q=.5",
 "application/rdf+xml;q=0.5,text/html;q=.5",
 rdfXml + "," + html,
 html + "," + rdfXml,
 rdfXml + ";q=0.5",
 html + ";q=0.5",
 xhtml + ";q=0.5"  ]

requestDescription = {
               rdfXml : "requesting RDF/XML data",
               html : "requesting HTML data",
               xhtml : "requesting XHTML data",
               xhtmlOrHtml : "requesting (X)HTML data"
               }

