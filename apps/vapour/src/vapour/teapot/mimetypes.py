rdfXml = "application/rdf+xml"
html = "text/html"

qualifiedRdfXml = "application/rdf+xml;q=0.5"
qualifiedHtml = "text/html;q=0.5"

mixedTypes1 = "application/rdf+xml;q=0.5,text/html;q=.3"
mixedTypes2 = "application/rdf+xml;q=0.3,text/html;q=.5"
mixedTypes3 = "application/rdf+xml;q=0.5,text/html;q=.5"

requestDescription = {
               rdfXml : "requesting RDF/XML data",
               html : "requesting HTML data",
               qualifiedRdfXml : "requesting RDF/XML with weights",
               qualifiedHtml : "requesting RDF/XML with weights"
               }