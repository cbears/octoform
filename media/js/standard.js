dojo.require("dojo.parser");
dojo.require("dijit.form.CheckBox");
dojo.require("dijit.form.DateTextBox");
dojo.require("dijit.form.Button");

dojo.require("dijit.layout.ContentPane");
dojo.require("dijit.Tree");
dojo.require("dojo.data.ItemFileReadStore");



function submitConnector( ) {
	dojo.query(".dateInputWidget").instantiate(dijit.form.DateTextBox,{ /* css? */ });
}

dojo.addOnLoad( submitConnector ) ;

