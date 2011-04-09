<%inherit file="question.mako" />
<%! from templates.html.encoding import markup %>

IF YOU ARE SEEING THIS IN A DOCUMENT, IT IS AN ERROR.
<%def name="header(q, state)"> <%
divisor = state["columns"] 
if divisor < 1:
	divisor=1
length=3.0/divisor
state["checkCount"] = 0
%>
% if state["form_has_errors"]:
% if field.errors:
    <DIV class="errors"> ${field.errors[0]} </DIV>
% endif
% endif

${q.label|markup} <BR>
</%def>

<%def name="footer(q, state)"> 
</%def>


<%def name="iter(choice, state)"> 
  <% 
  checked=""
  try:
    if choice[0] == state["data"]:
      checked="checked"
  except:
    pass
  state["checkCount"] += 1
  %>
	<DIV style="padding-left: 15px;">
	<input  type="radio"  					\
					name="${state["name"]}" \
					id="${state["id"]}_${state["checkCount"]}" \
					value="${choice[0]}"    \
					${checked} \
					dojoType="dijit.form.RadioButton" />
	&nbsp;
	${choice[1]|markup}  
	</DIV>
</%def>
