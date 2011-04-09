""" 
Berkeley Forms String Encodings.

We encode strings using markup. 

So for instance, My String |bold| Is bold |/bold| Not anymore. As a result,
everything coming into our system needs to have | replace by |||. We do a 
sub, changing ||| to __XX_BAD_XX__, strip on |, then change the inner tags
using the following. 

We also include the encoding function here, which is inappropriate.

"""

stringEncoding = { 
 'bold'   : '{\\bf ',
 '/bold'  : '}',
 'italic' : '{\\it ',
 '/italic': '}',
 'invert' : '\\begin{tikzpicture}[] \\path (.0,0.1) [white] node[shape=rectangle,fill=black,text width=6.5in] {',
 '/invert': '}; \\end{tikzpicture}',
 'br'     : ' \\\\* ',
 'indent' : '\hspace{.25in}',
 'small'  : '{\\small ',
 '/small' : '}',
 'large'  : '{\\large ',
 '/large' : '}',
 'larger' : '{\\Large ',
 '/larger': '}',
 'ul'     : '\\begin{tikzpicture} \\draw (0, -.05) -- (5.5, -0.05); \end{tikzpicture}',
 'ocr'    : """}; \\draw [use as bounding box] (0,0);
\\path (\\the\\pgf@picminx,\\the\\pgf@picmaxy) node[shape=circle,color=yellow,draw] (UpLeft)  {  } ;
\\path (\\the\\pgf@picmaxx,\\the\\pgf@picmaxy) node[shape=circle,color=yellow,draw] (UpRight) {  """

 
}

def markup( rawStr ): 
	if not rawStr:
		return ""
	markup = rawStr.replace( "|||", "__XX_BAD_XX__" ).replace( "\n", "" )
	newStr = []
	if markup.find("|") == -1:
		return rawStr.replace( "|||", "|" )
		
	i=0
	for tag in markup.split("|"):
		if i & 1:
			newStr.append( stringEncoding[tag.strip().lower()] )
		else:
			newStr.append( tag )
		i+=1
	return "".join(newStr).replace( "__XX_BAD_XX__", "|" )

