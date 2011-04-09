##
##     S E C T I O N 
##
<%
try: 
	state["layout"] = q.style["layout"]
except:
	q.style = {} # HACK!
	state["layout"] = "none"
layout = state["layout"]
%>																										\
% if q.style.has_key("start"):
  <%include file="section/${layout}_start"/>
% elif q.style.has_key("end"):
  <%include file="section/${layout}_end"/>
% endif 
##{% block itemHead %} {% endblock %}
