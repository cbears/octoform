# -*- coding: utf-8 -*-
"""
  " Low level routines which interact with (mako) template library)
  " (c) Charles Shiflett 2011
  "
  "" "" "" "" "" "" "" "" "" "" "" "" """

from mako.lookup import TemplateLookup
from mako import exceptions
from mako.exceptions import RichTraceback

import settings
import bfbdb
import bform
import logging

logging.basicConfig(level=logging.DEBUG)
log = logging.getLogger('forms.templateLoader')


class templateLookup: 
  """
  We used to use the Django/RoR standard of getTemplate / render_to_string.

  With Mako, and perhaps in general, it seemed to make more sense to return
  a template lookup object, which you can then use to generate a template.

  As a convenience, we re-produce some of the Django shortcuts, and, 
  implement a limited sort of caching.
  
  myLoader.render_to_string( "myTemplate", { 'myValue': 'baz' } )

  XXX: This looks increasingly like it should not exist here. Split into
       seperate file? -Bear

  """

  def __init__( self, themes=(), output="html" ):
    #from mako.template import Template
    if type(themes) == type(""):
      themes = ( themes, ) 
    if type(themes) != type(()):
      raise ValueError(" themes needs to be a tuple %s" % themes)
    self.state={ 'pgfCount': 0, 'log': logging.getLogger("MakoTemplate") }
    self.templates={}
    self.output=output
    dirs = []

    try: 
      for theme in themes+('default',):
        log.debug( "Theme: %s " % theme )
        dirs.append ( 
          "%(root)s/templates/%(output)s/themes/%(theme)s/" % 
            { 'root': settings.PROJECT_ROOT, 'output': output, 'theme': theme } 
        )
    except:
      log.warning("Err setting theme, could not parse %s." %  unicode(themes))

    log.debug("Debug: dirs=%s thms=%s format=%s" % (dirs, themes, output) )
    self.lookup = TemplateLookup( 
      directories=dirs, 
       input_encoding='utf-8',
      output_encoding='utf-8', 
      encoding_errors='replace')

  def render_to_string( self, template=False, values={} ):
    """ Automatically convert's a template BFORM_TYPE to a named type 
        if it exists in BFORM_TN """ 
    if not self.templates.has_key(template):
      # Messy hack for py 2.4
      if type(template) == type(1):
        template= "t%d" % template
      try: 
        log.debug("render_to_string translating template %s" % template)
        self.templates[template] = self.lookup.get_template(
          "%s.mako" % bform.BFORM_TN[int(template[1:])] ) 
      except:
        self.templates[template] = self.lookup.get_template( template )

    if type(values) != type( {} ):
      raise ValueError("render_to_string called with bad arguments (bad dict)") 

    rendered_template=""
    try: 
      rendered_template = self.templates[template].render_unicode(state=self.state, **values)
    except:
      log.exception(exceptions.text_error_template().render())
      traceback = RichTraceback()
      for (filename, lineno, function, line) in traceback.traceback:
        print "File %s, line %s, in %s" % (filename, lineno, function)
        print line, "\n"
      print "%s: %s" % (str(traceback.error.__class__.__name__), traceback.error)
      rendered_template = "Error: See log\n"
      raise

    return rendered_template

def renderContent( formId, alert=False,
       loadData=None, output="html", editable=False, form_has_errors=False,
       extra_context={}, getForm=bfbdb.loadObject, raw=False ):
  """
  renderContent renders all question/information associated with a form. After
  the form is rendered, all the data should be passed to renderPage, which
  finishes the rendering process.

  If you want validation errors to be shown as part of the rendering process,
  do:
    l=bform.bformData(bf, loadData)
    l.isValid()
    renderContent( ..., loadData=l )

  """

  tagNames = "baseFont" # CSV we want to copy over to template.

  "In case we are doing HTML output, we create a django form"
  bf = getForm( formId )
  if loadData.has_key('_initialized'):
    ld = loadData
  else:
    ld = bform.bformData( bf, loadData )

  ldr = templateLookup( themes=getattr(bf,'theme',()), output=output )
  formInfo = { 'formId': formId, 'form_has_errors': form_has_errors, 'alert': alert,'extra_context':extra_context }

  for tag in tagNames.split(","):
    if hasattr ( bf, tag ): 
      formInfo[tag] = getattr(bf,tag)

  return renderContentRecursive( 
    bf,ldr,formInfo,ld,editable,form_has_errors, raw=raw )
    
def renderContentRecursive( bf, ldr, formInfo, loadData, editable, form_has_errors, prefix="", suffix="", raw=False ):
  formOutput = []
  j=1
  for q in bf.Questions:
    if q.questionType == 1024: # Minipage
      try:
        count = int(loadData["q%03d" % j])
      except KeyError:
        count = 1

      if count < 1:
        count = 1

      partial = []

      for pageNumber in range( 0, count ):
        a,b,c = renderContentRecursive ( q.bForm, ldr, formInfo, loadData, editable, form_has_errors, "q%03d" % j, chr(ord('a') + pageNumber) ) 
        partial.append(c)
      formOutput.append( ldr.render_to_string ( "miniPage.mako", {
          'questionNumber': "q%03d"%j, 'content': "<HR>".join(partial), 'q': loadData["q%03d"%j]
        }) )
      j+=1
      continue

    questionId = "%sq%03d%s" % (prefix, j, suffix)
    try: 
      cntxt = { 'q': q, 'questionId': questionId, 
              'itemNumber': j, 
              'field': loadData[ questionId ], 
              'editable': editable,
              'form_has_errors': form_has_errors }
    except:
      cntxt = { 'q': q, 'questionId': questionId, 
              'itemNumber': j, 
              'editable': editable }
    formOutput.append( 
      ldr.render_to_string( q.questionType, cntxt ).replace("\t","")   )
    if q.questionType < 256:
      j+=1

  if (raw):
    return formOutput
  return bf, loadData, "".join(formOutput)

def renderPage ( page, bf, output='html', form_has_errors=False, barcode=False, alert=False, extra_context={}, hiddenFields=[]):
  passVars = locals()
  passVars.pop("bf")
  passVars.pop("output")
  ldr = templateLookup( themes=getattr(bf,'theme',()) , output=output )
  return ldr.render_to_string('baseForm.mako', passVars)
  #  { 'form_has_errors': form_has_errors, 'page': page, 'barcode': barcode, 'alert': alert } )  

def renderSpecial ( name, context, theme="", output="html"):
  """
  This is not a placeholder.
  """
  ldr = templateLookup( themes=theme , output=output )
  return ldr.render_to_string(name + ".mako", context )  

def jsCleanErrorMessage(message, id):
  return """ %(message)s
  <DIV style="cursor: pointer; cursor: hand; padding: 3px; color: blue" id="%(id)s_err"
     onclick="dojo.html.set('%(id)s_err', '<input type=\\'hidden\\' name=\\'%(id)s_ignore\\' id=\\'%(id)s_ignore\\' val=\\'1\\'/> Error cleared. ')">
   <center> <small> <u>clear error</u> </small>  </center>
  </DIV>
  """ % locals()

def makeForm( form, data ):
  from django.forms.util import ErrorList
  """
  XXX: replace
  """

  def clean(self):
    valid=True
    self.stupid_hack=False
    d = getData(self)
    for key,val in d.items():
      try: 
        if str(val) == "Data Mismatch." or (isinstance(val, list) and str(val[0]) == "Data Mismatch."):
          if self.fields.has_key(key) and isinstance(self.fields[key], forms.fields.ChoiceField) and True:
            "If we needed to clean anything up... "
            #self._errors[key] = ErrorList([jsCleanErrorMessage("Data Mismatch.",key)])
            self._errors[key] = ErrorList(["Data Mismatch."])
          else:
            self._errors[key] = ErrorList(["Data Mismatch."])
          valid=False 
      except Exception, e:
        log.debug("clean error (this can be safely ignored): %s (%s,%s) " % (e, key, val) )
        pass

    if not valid:
      raise forms.ValidationError("You can not submit this form")

  
  def getData(self):
    data = {}
    selfData = self.cleaned_data
    if not selfData:
      try:
        return self.stupid_hack
      except:
        pass
      if not self.data:
        return
      else:
        print "Warning, returning data because nothing else found"
        selfData = self.data
        
    for key, val in selfData.items():
      if isinstance(val, basestring) and not val:
        continue
      if val != None:
        data[key] = val

    for key,val in self.data.items():
      # Hidden fields don't get validated, so we need to re-add them.
      if key not in data:
        data[key]=val
    self.stupid_hack = data
    return data
  
  return type('NewForm', (forms.BaseForm,), {
    'base_fields': form.toDjangoForm(data), 'getData': getData, 'clean': clean} )
