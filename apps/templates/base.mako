<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01 Translational//EN" "http://www.w3.org/TR/html4/loose.dtd">
<html>

<head> <title> ${self.title()} </title>
	<style>
  		div.errors { 
			float: right; 
			border: solid 1px red; 
			background: #ffccdd;
			opacity: .9; 
			padding: 1px; 
			padding-right: 10px; 	
			padding-left: 10px; 
		} 
  </style>
  <meta http-equiv="content-type" content="text/html;charset=utf-8">
	${self.css()}
	${self.javascript()}
</head>

</head>
<body>
	<div class="container">
			
		<!-- Header -->
		<div id="header">
			${self.header()}
		</div>
		<div class="span-15 prepend-1 colborder">
			${self.body()}
		</div>
	<div class="span-7 last"> 
		${self.rightside()}
	</div>
	<hr class="space" />
	</div>
	%{self.footer()}
</body>
</html>
<%def name="css()">
	<link media="screen, projection" href="/media/themes/default/css/main.css" type="text/css" rel="stylesheet"/>
	<link media="screen, projection" href="/media/css/blueprint/screen.css" type="text/css" rel="stylesheet"/>
	<link media="screen, projection" href="/media/css/theme1.css" type="text/css" rel="stylesheet"/>
	<!--[if IE]> <link media="screen, projection>" href="/media/css/blueprint.ie.css" type="text/css" rel="stylesheet" <![endif]-->
</%def>

<%def name="header()">
<div id="logo" class="span-8">
		<h1><a href = "/"> Berkeley Forms </a></h1>
</div>
<div id="mainmenu">
	<div class="span-4">
			<a href ="/forms/"> Forms </a>
		</div>
		<div class="span-4">
				<a href = "/forms/list"> Scans </a>
		</div>
		<div class="span-4">
			<a href = "/media/docs/html/index.html"> Help </a>
		</div>
	</div>
</div>

<hr class="space" />
<hr>
</%def>
<%def name="body()"></%def>
<%def name="rightside()"></%def>
<%def name="footer()"></%def>
<%def name="javascript()"></%def>
<%def name="title()"></%def>

