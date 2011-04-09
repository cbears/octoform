<%page args="**kwargs"/> 											\
<%doc>
	This is our BASE template for non-question items,
</%doc> 	\
<% 
try:
  layout = q.style["layout"] 
except:
  try:
    layout = state["parentStyle"]
  except: 
    layout = "none"

state["layout"] = layout
state["style"] = getattr( q, "style", {})

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
  if hasattr("state", "default_columns"):
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
state["id"]   = getattr( field, "auto_id", "")

try:
  state["data"] = field.form.data[state["id"][3:]]
except:
  state["data"] = []


if state["columns"] > 6:
  state["columns"] = 6
%>	\
<%include 	file="${layout}/head_start"
<%include 	file="${layout}/head_start"
						args="state=state, q=q"/> 			\
	${self.header(q, state)}									\
<%include file="${layout}/head_end"
					args="state=state, q=q"/>					 
																						\
																						\
% for choice in q.choices:
  % if getattr(choice, "label", "") != "":
	  <%include file="${layout}/iter_start"
						args="state=state, q=q"/> 			\
		  ${self.iter(choice, state)}						\
	  <%include file="${layout}/iter_end" 
						args="state=state, q=q"/> 			\
  % endif
% endfor
${self.footer(state)}													\
<%include 	file="${layout}/footer"
						args="state=state, q=q"/> 			\
																						\
																						\
<%def name="header(q, state)"> </%def>			\
<%def name="iter(choice, state)"> </%def>		\
<%def name="footer(state)">   </%def>						\
