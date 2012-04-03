
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
            var report = get_vapour_report(uri.val());
            return false;
        } else {
            return false;
        }
    });

}

function get_vapour_report(uri) {
    try {
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
                                    alert(tests);
                                    var testsFailed = rdf.prefix("earl", "http://www.w3.org/ns/earl#")
                                                         .prefix("dc", "http://purl.org/dc/elements/1.1/")
                                                         .where("?testRequirement a earl:TestRequirement")
                                                         .where("?testRequirement dc:hasPart ?assertion")
                                                         .where("?assertion a earl:Assertion")
                                                         .where("?assertion earl:result ?result")
                                                         .where("?result earl:outcome earl:failed")
                                                         .length;
                                    alert(testsFailed);
                                });
    req.fail(function(response) { alert("Error: " + response.responseText); });
    } catch(e) { alert("Exception: " + e); }

}

