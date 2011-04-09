## -*- coding: utf-8 -*-
<%page args="**kwargs"/> \
<%doc>

 This is our BASE template, all HTML question should inherit it.
 
 Be careful with the terminology. In this context a header is just the first
 thing a question renders, and a footer is the last. For questions without
 choices, a header is pretty much all they need to implement.

 The code below should be a function call. Essentially, we are setting up
 the environment, which sadly, is required by Mako as it doesn't handle
 undefined items very well.

 Note:	This is adopted from the TeX template, and some things are awkward
 				or just don't make sense from the standpoint of HTML.

 Note:  The backslashes force Mako to ignore the newline at the end of
 				of the line. They aren't really needed for HTML.

 Note:  Uses two character tab spacing.

</%doc>\
<%text>
<!-- Question -->
</%text> <% 

try:
  layout = q.style["layout"] 
except:
  try:
    layout = state["parentStyle"]
  except: 
    layout = "none"

state["layout"] = layout
state["style"] = getattr( q, "style", {})
if field != Undefined: 
  state["value"] = field
else:
  state["value"] = ""
state["extras"] = ""

try: 
  state["itemNumber"] = int(itemNumber)
except:
  state["itemNumber"] = 0

# We have some convoluted ordering for trying to determine how many
# columns we should be using.
try: 
  state["columns"] = q.style["columns"]
  if q.style["columns"] < 1:
    print "div zero"
    bogus=1/0
except:
  if state.has_key("default_columns"):
    state["columns"] = state["default_columns"]
  else:
    try: 
      state["columns"] = len(q.choices)
    except:
      state["columns"] = 1

try: 
  state["log"].debug( "Item: %3d  Col: %3d  # Choices %3d " % 
    ( itemNumber, int(state["columns"]), len(q.choices) ) )
except:
  pass

state["column_count"] = 1

try:
  state["form_has_errors"] = form_has_errors
except:
  state["form_has_errors"] = False

state["name"] = getattr( field, "name"   , "")
if questionId != Undefined: 
  state["id"] = questionId
else:
  state["id"] = "UNKNOWN"

try:
  state["data"] = field.form.data[state["id"][3:]]
except:
  state["data"] = []


if state["columns"] > 6:
  state["columns"] = 6
output = []
%>	\

% if pageEditor:
<DIV class="question" 
     id="Dijit_${ state["id"] }"
     dojoType="dijit.layout.ContentPane" >
% endif

<%include 	file="${layout}/head_start"
						args="state=state, q=q"/> 			\

	${self.header(q, state)}									\
<%include file="${layout}/head_end"
					args="state=state, q=q"/>					 
																						\
																						\
% if hasattr(field, "field"):
  % if hasattr(field.field, "choices"):
  % for choice in field.field.choices:
	<%include file="${layout}/iter_start"
						args="state=state, q=q"/> 			
		${self.iter(choice, state)}
	<%include file="${layout}/iter_end" 
						args="state=state, q=q"/> 			
  % endfor
  % endif
% endif

${self.footer(q, state)}										\

<%include 	file="${layout}/footer"
						args="state=state, q=q"/> 			\
																						\
<%def name="header(q, state)">							\
	${q.label} <BR>
  % if state["form_has_errors"]:
  <DIV class="errors"> XXX: show errors </DIV>
  % endif
</%def>																			\
																						\
<%def name="iter(choice, state)">		\
	${choice}
</%def>																			\
																						\
<%def name="footer(q, state)">							\
</%def>																			\

% if pageEditor:
  </DIV>
% endif 
