<%inherit file="infoBase.mako"/>

<%! from templates.html.encoding import markup %>

<%def name="header(q, state)">
<h1>${ q.label|markup }</h1></%def>
