
/* vapour js scripts */

function example() {
    $("tt#example").click(function() {
        $("input#vocabUri").val($("tt#example").html());
    });
}

function cleanInputs() {
    var inputs = new Array("vocab", "class", "property", "instance");
    for (var i=0; i<inputs.length; i++) {
        var input = $("#"+inputs[i]+"Uri");
        input.focus(function() { 
            if($(this).val()=="http://") {
                $(this).val();
            }
        });
        input.blur(function() { 
            if(!$(this).val()) {
                $(this).val("http://"); 
            }
        });
    }
}

function showHideForms() {
    $("#vocabularyValidationLegend").click(function() { 
        showHide($(this), "vocabularyValidationSubform"); 
    });
    $("#advancedOptionsLegend").click(function() { 
        showHide($(this), "advancedOptionsSubform"); 
    });
}

function showHide(element, name) {
    var div = $("#"+name);
    if (div.is(":hidden")) {  
        element.css("background-image", "url('http://vapour.sourceforge.net/resources/arrow-open.png')");
        div.slideDown("slow");
    } else {
        element.css("background-image", "url('http://vapour.sourceforge.net/resources/arrow-closed.png')");
        div.slideUp("slow");
    }
}

function submit() {
    $.validator.addMethod("notonlyhttp", 
        function(value, element) {
            return (value != "http://");
        }, 
        "URI required!"
    );
    var form = $("form#form");
    form.validate({
        rules: {
            vocabUri: {
                required: true,
                notonlyhttp: true
            }
        }
    });
    $("#checking-dialog").dialog({
        dialogClass: "alert",
        autoOpen: false,
		modal: true,
		resizable: false,
        width:'auto',
		draggable: false
	}).siblings(".ui-dialog-titlebar").remove();
    form.submit(function() {
        if ($(this).valid()) {
            var button = $("#submitButton");
            button.attr("disabled", "disabled");
            $('#checking-dialog').dialog('open');
            button.val("Checking...");
        } else {
            return false;
        }
    });
}

$(document).ready(function() {
    example();
    cleanInputs();
    showHideForms();
    submit();
});

