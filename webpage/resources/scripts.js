
/*
  vapour.sf.net scripts
*/

function example() {
	var node = document.getElementById("example");
	node.onclick = function() { document.getElementById("vocabUri").value=this.innerHTML };
}

function cleanInputs() {
    var inputs = new Array("vocabUri", "classUri", "propertyUri", "instanceUri");
    for (var i=0; i<inputs.length; i++) {
        var input = document.getElementById(inputs[i]);
        input.onfocus = function() { if(this.value=='http://') this.value=''; };
        input.onblur = function() { if(this.value=='') this.value='http://'; };
    }
}

function showHideForm() {
    //vocabulary validation legend
    var vocabularyValidationLegend = document.getElementById("vocabularyValidationLegend");
    vocabularyValidationLegend.onclick = function() { showHide(vocabularyValidationLegend, document.getElementById('vocabularyValidationSubform')); };

    //vocabulary validation legend
    var advancedOptionsLegend = document.getElementById("advancedOptionsLegend");
    advancedOptionsLegend.onclick = function() { showHide(advancedOptionsLegend, document.getElementById('advancedOptionsSubform')); };
}

function addLoadEvent(func) {
	//by Simon Willison:
	//   http://simon.incutio.com/archive/2004/05/26/addLoadEvent
	var oldonload = window.onload;
	if (typeof window.onload != 'function') {
		window.onload = func;
	}
	else {
		window.onload = function() {
			oldonload();
			func();
		}
	}
}

addLoadEvent(example);
addLoadEvent(cleanInputs);
addLoadEvent(showHideForm);

