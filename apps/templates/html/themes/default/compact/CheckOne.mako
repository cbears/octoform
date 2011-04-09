<%inherit file="question.mako" />
<%! from bforms.templates.html.encoding import markup %>

IF YOU ARE SEEING THIS IN A DOCUMENT, IT IS AN ERROR.
<%def name="header(q, state)"> <%
divisor = state["columns"] 
if divisor < 1:
	divisor=1
length=3.0/divisor
%>
${q.label|markup} <BR>
<select name="${state["name"]} id="${state["id"]}" >
</%def>

<%def name="footer(q, state)"> 
% if state["form_has_errors"]:
% if field.errors:
    <DIV class="errors"> ${field.errors[0]} </DIV>
% endif
% endif
</select>
</%def>


<%def name="iter(choice, state)"> 
  <% 
  checked=""
  try:
    if choice[0] == state["data"]:
      checked="checked"
  except:
    pass
  %>
	<DIV style="padding-left: 15px;">
  <option name="${state["name"}" id="${state["id"]}" value="${choice[0]}" ${checked} >
	&nbsp;
	${choice[1]|markup}  
  </option>
	</DIV>
</%def>
