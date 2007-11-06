
/*
  vapour.sf.net scripts
*/

function example() {
	var node = document.getElementById("example");
	node.onclick = function() { document.getElementById("vocabUri").value=this.innerHTML };
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

