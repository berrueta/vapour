
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
                        dataType: "text"
                     });
    req.done(function(response) {
                                    alert(response);
                                    var rdf = $.rdf().load(response, {});
                                    var tests = rdf.prefix("earl", "http://www.w3.org/ns/earl#")
                                                   .where("?testRequirement a earl:TestRequirement");
                                    alert(tests.length);
                                });
    req.fail(function(response) { alert("Error: " + response.responseText); });
    } catch(e) { alert("Exception: " + e); }

}

