<%page args="**kwargs"/> \
<%doc>

 This is our BASE template, all TeX questions should extend it, You may use
   itemHead, itemIter, & ItemFoot. itemIter iterates over choices.

 This template inserts positional information for OCR into the TeX templates.

 The specifics of it will change with time...

 ToDo: 
 	* We might like more of a start point and a height/width 
	* Regular question position is not recorded.

 First record the question we are creating.
   Everything gets stored in a text file. When we are done we re-read the text
   file to "remember" everything we have done. Using the file we just created,
   we read in our variable names, determine positional information, and then
   re-write a file with that positional information.

 What else:
 	 The overall structure should be Types extend this base, which is then
	 extended by layout information. 

</%doc>\
<%text>
% THIS IS THE BASE QUESTION TEMPLATE. 
%                 _   |~  _
%                [_]--'--[_]
%                |'|""`""|'|
%                | | /^\ | |
%          jgs   |_|_|I|_|_|
%
%
</%text> <% 
try:
	layout = q.style["layout"] 
except:
	layout = "none"

state["layout"] = layout

try:
	state["style"] = q.style
except:
	state["style"] = {}

try: 
	state["itemNumber"] = itemNumber
except:
	state["itemNumber"] = "NotDefined"

"""
	Some variables we set statically. In some cases, we may want to restore
	them after setting them. We can start with this, and go from there.
"""

# We have some convoluted ordering for trying to determine how many
# columns we should be using.
try: 
	state["columns"] = q.style["columns"]
except:
	if hasattr("state", "default_columns"):
		print "DID default columns"
		state["columns"] = state["default_columns"]
	else:
		try: 
			state["columns"] = len(q.choices)
		except:
			state["columns"] = 1
		
try: 
	print "I: ", itemNumber, " C: ", state["columns"], "L: ", len(q.choices)
except:
	pass
state["column_count"] = 1
	
%>	\
\setcounter{sub_item}{0}
\immediate\write5{***} 
<%include 	file="${layout}/head_start"
						args="state=state, q=q"/> 			\
	${self.header(q, state)}									\
<%include file="${layout}/head_end"
					args="state=state, q=q"/>					 
																						\
																						\
% for choice in q.choices:
##	${choice.label}
	\addtocounter{sub_item}{1} 								\
	<%include file="${layout}/iter_start"
						args="state=state, q=q"/> 			\
		${self.iter(choice, state)}							\
	<%include file="${layout}/iter_end" 
						args="state=state, q=q"/> 			\
	\immediate\write5{q${itemNumber}\alph{sub_item}} 
% endfor
${self.footer(state)}														\
<%include 	file="${layout}/footer"
						args="state=state, q=q"/> 			\
																						\
<%def name="header(q, state)">							\
	\vspace{\baselineskip}
	\begin{minipage}[t]{0.25in} ${itemNumber}.  \end{minipage}
	\begin{minipage}[t]{6in}    ${q.label}
	\vspace{0.5em}
</%def>																			\
																						\
<%def name="iter(choice, state)">						\
##	\begin{comment} 
##	Default choice, did you really want this? 
##	\end{comment}
  \begin{minipage}[t]{.25in} \alph{sub_item}. \end{minipage}
  \begin{minipage}[t]{  6in} 
	${choice.label}
	\end{minipage}
  \begin{minipage}[t]{  .5in} 
			\begin{tikzpicture} 
        \draw [use as bounding box] (1,1)  ;
				\path (2,1.1) node[shape=circle,color=yellow,draw] (q${itemNumber}\alph{sub_item}) {  } ; 
				\draw[blue]  (1.85,1.15)  -- (1.8,1.1)  -- (1.85,1.05);
				\draw[blue]   (2.1,1.15)  -- (2.15,1.1) -- (2.1,1.05);
				\path (2.3,1.05) node { \tiny \textit{\alph{sub_item} } };
			\end{tikzpicture} 
			\hspace{\stretch{1}}
 	\end{minipage}
	\vspace{0.2em}
</%def>																			\
																						\
<%def name="footer(state)">											\
	\end{minipage}
</%def>																			\
