dojo.require("dojo.parser");
dojo.require("dijit.InlineEditBox");
dojo.require("dijit.form.TextBox");
dojo.require("dijit.layout.ContentPane");
dojo.require("dijit.form.ComboBox");
dojo.require("dojo.data.ItemFileReadStore");

// (c) Charles Shiflett 2011

var submitData = [] 
var submitEntry = 0
var labelKeys = []
var choiceKeys = []

/* Utility Functions */
function zeroPad ( num ) {
	num = ( num - 1 ) + 1

	if (num  < 10) {
		num = "0" + num 
	}
	if (num  < 100) {
		num  = "0" + num 
	}

	return num; 
} 
/* end utility functions */

function addPlaceholder() {
	console.debug ("addPlaceholder: " + currentFocus)
	var item = currentFocus.substr(1)

	if ( item.length > 4 ) {
		var tmp = item.split("c")
		item = tmp[0]
	}

	item = "Did_q" + zeroPad(item) 
	console.debug("Item: "+ item)

	dijit.byId(item).attr('content', dijit.byId(item).attr('content') + 
		"<DIV style='border: solid 1 px black'> " + 
		"	Added Choice -- Please update to see change. " +
		"</DIV>" )

}

function swapItem (moveDirection) {
	var moveTo   = currentFocus.substr(1)
	var moveFrom = currentFocus
	var prefix   = "Did_q"
	var swapType = "question"

	console.debug (" Swap Item called with: " +moveTo+ " " + moveDirection )

	if ( moveTo.length > 4 ) {
		swapType = "choice"
		var tmp = moveTo.split("c")

		prefix = prefix + zeroPad(tmp[0]) + "c"
		moveTo = tmp[1]

	}

	moveTo -= 1  // "Move UP" 
	if ( moveDirection == "down" ) {
		moveTo += 2
	}
	moveTo = zeroPad ( moveTo ) 

	if ( !dijit.byId(prefix + moveTo) ) { 
		console.debug("Tried to swap with non-existant widget, abort.");
		return 
	}


	// swap
	removeConnectors() 

	var oldW = dijit.byId("Did_" +moveFrom ).attr('content') 
	var newW = dijit.byId(prefix +moveTo   ).attr('content') 

	dijit.byId("Did_" +moveFrom ).attr('content', "")
	dijit.byId(prefix +moveTo   ).attr('content', "")

	dijit.byId("Did_" +moveFrom ).attr('content', newW)
	dijit.byId(prefix +moveTo   ).attr('content', oldW)   

	loadConnectors()

	// adjust focus
	loseFocus( "Did_" + moveFrom )
	showFocus( prefix + moveTo   )

	// make a note of our move.
	var sIndex = submitEntry
	submitEntry += 1

	submitData[ sIndex ]  =  
		[sIndex, "move " + swapType, moveFrom, moveTo];

}

function newQuestionLabel(qId, questionValue) {
	var questionId = qId.substr(4)
	console.debug("New label for " + questionId + " is now "+questionValue);

	var sIndex = submitEntry
	submitEntry += 1

	var editAction = "form label"

	if ( questionId.length > 6 ) 
		editAction = "form choice";
		
	submitData[ sIndex ]  =  
		[sIndex, editAction, questionId, questionValue];
	console.debug ( submitData )
}

var alreadyEdited = []
var currentFocus = ""
var lastFocus    = "" // Not really last focus, more like most recent focus.

function updateToolbar ( aName, aId ) {
	console.debug("update "+ aName +" "+ aId)
}

function showFocus( dijitId ) {
	if (currentFocus) {
		loseFocus( "Did_" +  currentFocus )
	}

	var questionId =  dijitId.substr(4)
	lastFocus    = questionId
	currentFocus = questionId

	console.debug ( "Focus on:" + questionId )

	if ( dijitId.length < 10 ) {
		dijit.byId(dijitId).attr ('style', 'background: yellow' );
	} else {
		dijit.byId(dijitId).attr ('style', 'background: orange' );
	}

	if (questionId.length == 4 ) {
		dijit.byId("id_questionType").attr('value',Everything[questionId].questionType);
		dijit.byId("id_label").attr('value',Everything[questionId].label);
		// XXX: need to check if string first.
		
		console.debug ( questionId )
		console.debug ( "Type: " + Everything[questionId].questionType )

		// We should be highlighted all picked items in a combo box, you can
		// then delete highlighted items, edit already selected items, or, 
		// add previously un-added items. We only have one box, but we 
		// implicitly allow adds/edits/etc. 
		//

		/* We just need to update the styles here... Only update the labels 
		 * if something relevant is already selected.
		 *

		var tmp=0
		if (Everything[questionId].style) {
			tmp = Everything[questionId].style[0]
		} 

		if (tmp) {
			dijit.byId("id_styleType").attr ('value',tmp[0])
			dijit.byId("id_styleArgs").attr('value',tmp[1])
		} else { 
			dijit.byId("id_styleType").attr ('value','')
			dijit.byId("id_styleArgs").attr('value','')
		}

		tmp=0
		if (Everything[questionId].constraints) {
			tmp = Everything[questionId].constraints[0]
		} 

		if (tmp) {
			dijit.byId("id_conType").attr   ('value',tmp[0])
			dijit.byId("id_conArgs").attr  ('value',tmp[1])
		} else {
			dijit.byId("id_conType").attr   ('value',"")
			dijit.byId("id_conArgs").attr  ('value',"")
		}

		*/ 

		
	} else {
		console.debug("Not updating ancillary info... nothing to do...")
	}

}

function loseFocus( dijitId ) {
	var questionId =  dijitId.substr(4)

	// XXX: un-setting currentFocus might make things *not* work as expected.
	var currentFocus = ""

	console.debug ( "unFocus on:" + questionId )

	dijit.byId(dijitId).attr ('style', 'background: none');
}

/* 
 * DEPRACATED. Replaced by generic property routines. We could bring it back
 *             but, we would have to unload the widget before form modification
 *//*
function editValue( e ) {
	if ( !e.currentTarget || !e.currentTarget.id ) {  
		console.debug (" Got an empty ... ");
	  return ; 
	}
				
	var questionId =  e.currentTarget.id.substr(4)
	var dijitId    =  e.currentTarget.id

 	if (alreadyEdited[questionId]) {
	  return 
	}

	if (questionId.length > 6) { 
		dijit.byId ( dijitId ).value = "" + choiceValues [ questionId ]
		alreadyEdited[ questionId ]  = choiceValues [ questionId ]
	} else {
		// standard label
		dijit.byId ( dijitId ).value = "" + labelValues [ questionId ]
		// "dijit[*].value" only supports strings
		alreadyEdited[ questionId ]  = labelValues [ questionId ]
	}

	// should be alreadyEdited[ questionId ] = sequence
}
*/

function submitForm( e ) {
	// should use introspection to figure out which form to submit... if any.
	dojo.xhrPost ({
		url: './',
		handleAs: 'json',
		form: "addQuestion",
		content: { jscriptData: dojo.toJson(submitData) } ,
		timeoutSeconds: 3,
		timout: function(type, data, evt) { 
			 console.error ("boot: Too SLOW!"); 
		},

		load: function (data) {
			removeConnectors() 
			dijit.byId('contentNode').attr ( 'content', data.formContent )

			labelValues = data.labels
			choiceValues = data.choices

			loadConnectors() 
		},

		error: function (error, ioargs) {
			console.error ('Error: ', error );

			// Show the error that just occurred. Debugging Code.
			dijit.byId('contentNode').attr ( 'content', error.responseText ) ;
		}

	}); // end dojo.xhr post
	return false;
}

function setVal( e ) {
	if ( !e.length ) {
		console.debug( "setVal called with bad args. ")
		return ; 
	} 
	console.debug("You set "+ e +" to "+ dijit.byId("id_"+ e).value +' for '+ lastFocus) 
	// We should probably take some sort of filtering action here...
	var sIndex = submitEntry
	submitEntry += 1

	var editAction = "form " + e
	submitData[ sIndex ]  =  
		[sIndex, editAction, lastFocus, dijit.byId("id_" + e).value];

	console.debug(submitData)
}

var store = new dojo.data.ItemFileReadStore({data: Everything["q001"]});

// ****************************************************************
//
//      CONNECTOR RELATED ------------------ BELOW HERE
//
// ****************************************************************

function makeKeys() {
			var i = 0
	    for (lKey in labelValues) { 
				labelKeys [i] = lKey
				i = i+1
			}
			labelKeys = labelKeys.sort()
			i = 0
	    for (cKey in choiceValues) { 
				choiceKeys [i] = cKey
				i = i+1
			}
}

function submitConnector( ) {
	dojo.connect(dojo.byId("formToSubmit"), 'onsubmit', submitForm ); 
}

function editConnector() {
	/* editValue is depracated, so clearly we don't need the connectors.
	 * We could change the focus if you click on the label or choice, but
	 * for now, we just do nothing.
	 *
	 */
	return new Array ();
}

function focusHelper(  questionId ) {
	dijitObject = dijit.byId( "Did_"+questionId ) 
	var c = new Array(2);

	c[0] = dojo.connect(
		dijitObject,	
		'onFocus', 
		new Function("{ showFocus('Did_"+ questionId +"'); }")
	);

	c[1] = dojo.connect(
		dijitObject,	
		'onBlur', 
		new Function("{ loseFocus('Did_"+ questionId +"'); }")
	);

	return c;

}


function focusConnector() {
	var c = new Array(labelKeys.length + choiceKeys.length*2); 
	var a = []; 

	for (var i=0; i < labelKeys.length ; i++) {
		a = focusHelper(labelKeys[i])
		c [ i * 2 ] = a [0]
		c [ i*2+1 ] = a [1]
	}

	for (var i=0; i < choiceKeys.length; i++) {
		a = focusHelper(choiceKeys[i])
		c[(i+labelKeys.length) * 2] = a[0]
		c[(i+labelKeys.length)*2+1] = a[1]
	}

	return c;
}

var connectors = [];
function loadConnectors() {

	makeKeys()

	connectors = focusConnector() 

	// almost shouldn't return a value, as we set a global variable connectors.
	return connectors
}

function removeConnectors() {
	for (var i=0; i < connectors.length; i++) {
		dojo.disconnect(connectors[i])
	}
	connectors = []
}

connectors = dojo.addOnLoad( loadConnectors ) ;

dojo.addOnLoad( submitConnector ) ;

dojo.connect(
  dojo.byId("contentNode"), 
	'onkeypress',

	function(e) {
		if (currentFocus) {
			console.debug ( "Char Code: " + e.charCode )
			if (e.charCode == 65) {
				console.debug(' adding a place holder for editing ')
				var sIndex = submitEntry
				submitEntry += 1

				submitData[ sIndex ]  =  
					[sIndex, "add  choice", currentFocus, "" ];

				addPlaceholder()
			}
			if ( (e.keyCode == dojo.keys.UP_ARROW  ) ||
			     (e.keyCode == dojo.keys.DOWN_ARROW) ) {

				var moveDirection = "up"
				if (e.keyCode == dojo.keys.DOWN_ARROW ) {
					// If you aren't careful... Doing a plus will concatonate, where
					// as minus always does integer subtraction.
					moveDirection = "down"
				}
				swapItem ( moveDirection );

			}
		}

	}   
);



