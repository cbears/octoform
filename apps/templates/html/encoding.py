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
 'bold'   : '<B> ',
 '/bold'  : '</B>',
 'underline'   : '<U> ',
 '/underline'  : '</U>',
 'italic' : '<I>',
 '/italic': '</I>',
 'invert' : '<DIV STYLE="background: black; color: white">',
 '/invert': '</DIV>',
 'br'     : '<BR>',
 'indent' : '&nbsp;&nbsp;&nbsp;&nbsp;',
 'small'  : '<!-- Start SMALL -->',
 '/small' : '<!-- End   SMALL -->',
 'large'  : '<H2> ',
 '/large' : '</H2>',
 'larger' : '<H1> ',
 '/larger': '</H1>',
 'ocr'    : ''

 
}

def markup( rawStr ): 
  if not rawStr:
    return ""
  
  if type(rawStr) != type(u""):  
    print "Error, RawStr=%s, should be UNICODE" % type(rawStr)

  markup = rawStr.replace( u"|||", u"__XX_BAD_XX__" ).replace( u"\n", "" )
  newStr = []
  if markup.find(u"|") == -1:
    return rawStr.replace( u"|||", u"|" )
    
  i=0
  for tag in markup.split(u"|"):
    if i & 1:
      newStr.append( stringEncoding[tag.strip().lower()] )
    else:
      newStr.append( tag )
    i+=1

  retVal = u"".join(newStr).replace( "__XX_BAD_XX__", "|" )
  try:
    return unicode(retVal, "utf-8", errors='replace')
  except:
    return retVal

