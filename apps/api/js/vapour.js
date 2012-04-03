
jQuery.fn.vapour = function() {

    var form = $(this);

    form.validate({
        rules: {
            uri: {
                required: true,
                url: true
            }
        }
    });

    form.submit(function() {
        if ($(this).valid()) {
            var uri = form.find("input#uri");
            getVapourReport($(this), uri.val());
            return false;
        } else {
            return false;
        }
    });

}

function getVapourReport(form, uri) {

    var req = $.ajax({
                        type: "GET",
                        //url: "http://validator.linkeddata.org/vapour", 
                        url: "http://localhost:8000/vapour",
                        contentType: "application/x-www-form-urlencoded",
                        data: { vocabUri: uri, format: "rdf" },
                        accepts: "application/rdf+xml",
                        dataType: "xml"
                     });

    req.done(function(response) {
                                    var rdf = $.rdf().load(response, {});
                                    var triples = rdf.databank.size();
                                    var tests = rdf.prefix("earl", "http://www.w3.org/ns/earl#")
                                                   .where("?testRequirement a earl:TestRequirement")
                                                   .length;
                                    var testsFailed = rdf.prefix("earl", "http://www.w3.org/ns/earl#")
                                                         .prefix("dc", "http://purl.org/dc/elements/1.1/")
                                                         .where("?testRequirement a earl:TestRequirement")
                                                         .where("?testRequirement dc:hasPart ?assertion")
                                                         .where("?assertion a earl:Assertion")
                                                         .where("?assertion earl:result ?result")
                                                         .where("?result earl:outcome earl:failed")
                                                         .length;
                                    var testsPassed = tests - testsFailed;
                                    var report = new Object();
                                    report.uri = uri;
                                    report.tests = tests;
                                    report.testsPassed = testsPassed;
                                    report.testsFailed = testsFailed;
                                    printVapourReport(form, report);
                                });

    req.fail(function(response) { 
                                    alert("Vapour JS Error: " + response.responseText); 
                                });

}

function printVapourReport(form, report) {
    var color = (report.testsFailed == 0) ? "green" : "red";
    var style = "background-color: " + color + "; color: #ffffff; padding: 0.5em 1em 0.5em 1em; width: auto; text-align: center; border-radius: 6px;";
    form.after("<p style=\"" + style + "\"> " + report.testsPassed + " / " + report.tests + " </p>");
}

