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
<DIV style='margin-left: 50px'> 
${q}
</DIV>

</%def>


<%def name="iter(q, state)"> 
</%def>
