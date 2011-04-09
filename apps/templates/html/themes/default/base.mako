<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01//EN"
            "http://www.w3.org/TR/html4/strict.dtd">
<html>
<head> 
<meta http-equiv="content-type" content="text/html;charset=utf-8">
<title> ${self.title()} </title>
	${self.css()}
	${self.javascript()}
  ${self.extrajavascript()}
  </head>
	
		<div class="header">
				${self.header()}
			</div>
		<div class="body">
					${self.body()}
		</div>
	  <div class="footer">
				${self.footer()}
		</div>
			
		</div>
		
	</body>
</html>

<%doc>
	Here we define the default behavior of the pages that inherit from base.mako
</%doc>
<%def name="footer()">
</%def>
<%def name="header()">
</%def>
<%def name="css()">
  <style type="text/css">
    @import "/media/js/dijit/themes/tundra/tundra.css";
    @import "/media/js/dojo/resources/dojo.css";
  </style>
<link media="screen, projection" href="/media/themes/default/css/main.css" type="text/css" rel="stylesheet"/>
<link media="screen, projection" href="/media/css/blueprint/screen.css" type="text/css" rel="stylesheet"/>
<link media="screen, projection" href="/media/css/theme1.css" type="text/css" rel="stylesheet"/>

    

</%def>
<%def name="javascript()">
  <script type="text/javascript" src="/media/js/dojo/dojo.js"
          djConfig="parseOnLoad: true"></script>
  <script type="text/javascript" src="/media/js/standard.js"></script> 
</%def>
<%def name="extrajavascript()"></%def>
<%def name="title()">
</%def>	
<%def name="rightside()">
</%def>
<% rightside=False %> 
