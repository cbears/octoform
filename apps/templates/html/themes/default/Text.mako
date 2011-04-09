<%inherit file="question.mako"/>
<%! from templates.html.encoding import markup %>

IF YOU ARE SEEING THIS IN A DOCUMENT, IT IS AN ERROR.

<%def name="header(q, state)"> 
% if state["form_has_errors"]:
% if field.errors:
    <DIV class="errors"> ${field.errors[0]} </DIV>
% endif
% endif
${q.label|markup}
</%def>


<%def name="footer(q, state)"> 
    <input id="${"id_%s" % state['id']}" type="text" name="${"id_%s" % state['id']}" value="${state['value']}" ${state['extras']} />
</%def>


<%def name="iter(q, state)"> 
</%def>
