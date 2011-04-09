<%page args="**kwargs"/> 											\
<%doc>

 This is our BASE template, all TeX questions should extend it, You may use
   itemHead, itemIter, & ItemFoot. itemIter iterates over choices.

</%doc> 																			\
## This nice little graphic gets in the way of rendering our
## TeX document. Maybe it is an evil graphic.
## <%text>
## % THIS IS THE INFO QUESTION TEMPLATE. 
## %       /---------\
## %      /  __   __  \
## %     /  / o   o \  \   Darth Info.
## %    /       ^       \
## </%text> 																			
<% 
try: 
	layout = q.style["layout"] 
except: 
	layout="none"

try: 
	state["style"] = q.style
except:
	state["style"] = {}
%>																					\
<%include 	file="${layout}/head_start"
						args="state=state, q=q"/> 			\
	${self.header(q, state)}									\
<%include file="${layout}/head_end"
					args="state=state, q=q"/>					 
																						\
																						\
% for choice in q.choices:
	<%include file="${layout}/iter_start"
						args="state=state, q=q"/> 			\
		${self.iter(choice, state)}							\
	<%include file="${layout}/iter_end" 
						args="state=state, q=q"/> 			\
% endfor
${self.footer(state)}														\
<%include 	file="${layout}/footer"
						args="state=state, q=q"/> 			\
																						\
																						\
<%def name="header(q, state)"> </%def>			\
<%def name="iter(choice, state)"> </%def>		\
<%def name="footer(state)">   </%def>						\
