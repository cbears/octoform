<%inherit file="question.mako" />
<%! from templates.tex.encoding import markup %>

IF YOU ARE SEEING THIS IN A DOCUMENT, IT IS AN ERROR.

<%def name="header(q, state)"> <%
divisor = state["columns"] 
if divisor < 1:
	divisor=1
length=3.0/divisor
%>
${q.label|markup}
</%def>


<%def name="footer(state)"> 
</%def>


<%def name="iter(choice, state)"> 
  <% 
  smoo = u'突' 
  smoo = unicode( choice.label, errors='replace' )
	%>
	${smoo}
</%def>
