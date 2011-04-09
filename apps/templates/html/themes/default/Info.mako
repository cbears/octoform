<%inherit file="infoBase.mako"/>

<%! from templates.html.encoding import markup %>

<%def name="header(q, state)">
${ q.label|markup }</%def>
<%def name="iter(choice, state)">
${ choice.label|markup } 
</%def>
