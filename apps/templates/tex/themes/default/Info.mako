<%inherit file="infoBase.mako"/>

<%! from templates.tex.encoding import markup %>

<%def name="header(q, state)">
${ q.label|markup }</%def>
<%def name="iter(choice, state)">
<% print "I. Choice: ", choice %>

${ choice.label|markup } 

</%def>
