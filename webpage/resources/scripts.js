
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

$(document).ready(function() {
    example();
    cleanInputs();
    showHideForms();
});

