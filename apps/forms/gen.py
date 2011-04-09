# -*- coding: utf-8 -*-
"""
  " Routines to generate forms
  " (c) Charles Shiflett 2011
  "
  "" "" "" "" "" "" "" "" "" "" "" "" """


# This needs to be moved to a better location.
import form_models.bfbdb as bfbdb
import form_models.bform as bform
import form_models.bfsql as bfsql
import form_models.templateLoader as templateLoader
import form_models.util as util

import random
import re
import utils

import settings

hNewIds, hOldIds = [], []

def bForm( request, formId, refNo=None, barcode=False, Alert=False ):
  """
  View a form, or, save/load data from a form.

    * formId    = The Berkeley Form Id of the form to be loaded
    * refNo     = The Ref No. associated with the berkeley 
    * request   = The POST data associated with a request.
                  (request = dict(lite(django request object)) )
    
    bf, df = berkeleyForm, djangoForm

  How we handle reference #'s needs to be thought out. I.e. should our
  interface to reference numbers increment automatically? I'm thinking
  it should be:
    1) Each update references the original reference #
    2) BerkleyDB maintains index of all root Ref #'s, s/t we can
       quickly determine where the newest version is.
       -- s bdb trans ->  s postgres trans -> commit postgres -> commit bdb
       -- we could avoid the mess by overwriting old data, which is bad.

  """
  miniNum=False
  hiddenFields=[]
  loadData = {}

  if request['method'] != 'POST': # If request != POST it is the initial form load
    "Generate form check # to prevent dup's & generate hash for bogus submits."
    hiddenFields= [ ('hId', util.genString(23)) ]
    if hiddenFields[0][1] in hNewIds:
      raise ValueError("hiddenFields[0][1] in hNewIds")
      return bForm(request, formId, refNo=refNo, barcode=barcode, Alert=Alert)
    hiddenFields.append( ('hCheck', util.hash(hiddenFields[0][1]) ) )
    hNewIds.append(hiddenFields[0][1])

  """ Check to see if the user requested that we load data into the form 
      through either POST (highest precedence), reference #, or barcode """

  if request['method'] == 'POST': 
    loadData = request['POST']

  elif refNo:
    loadData = dict( bfsql.getForm(formId, refNo) )

  if not Alert:
    if refNo and not loadData:
      Alert="WARNING: Ref # %s contained no data." % refNo
    # If alert, we already rendered bf, df, & page. Otherwise do normal render.
    bf, df, page = templateLoader.renderContent(formId,loadData=loadData)

  form_has_errors = False
  if request['method'] == 'POST':  
    data, miniNum = utils.handleMinipage( df, loadData )
    if miniNum: # Adding or removing a mini-page
      bf, df, page = templateLoader.renderContent(formId,loadData=data)
    else: # Do the standard submit.
      dfValid = df.is_valid()

      if dfValid: # Check that the submission is not a duplicate
        dfData = df
        if dfData["hId"] in hNewIds and dfData["hId"] not in hOldIds and \
           dfData["hCheck"] == util.hash(dfData["hId"]): 
          hOldIds.append(dfData["hId"])

        elif not settings.debug: # It is a duplicate generate an error.
          Alert= """ <B> Error: </B> 
                         Form can not be submitted because it has already been
                         submitted or the form has expired. <BR> <BR> &nbsp;
                         &nbsp; <I> To submit this form, go back to the scans 
                         list, and re-load this form. </I>
                 """
          dfValid=False

      if dfValid:
        refno = bfsql.insertForm( formId, df.getData() ) 
        " Success indicator, should be configurable "
        return templateLoader.renderSpecial( "refNo", {"refno": refno, "formno": formId } )
      elif not Alert:  
       form_has_errors = True
       "We just set form_has_errors=True, thus need to re-render the page"
       bf, df, page = templateLoader.renderContent(
         formId,loadData=loadData, form_has_errors=form_has_errors )
       print "Tried Insert, but form was NOT VALID! (", loadData, ")" 

  # The rendered content is already in page, renderPage adds the final
  #  decorations (i.e. page borders). Theme from bf, which is otherwise unused.
  return templateLoader.renderPage( page, bf, form_has_errors=form_has_errors, barcode=barcode, alert=Alert,extra_context={'miniNum':miniNum}, hiddenFields=hiddenFields )

"""
def currentForm( request, refNo):
  IDs, dontcare = bfsql.getFormIdByBarcode(refNo)
  bForm( request, IDs[-1][1], formId)
"""

if __name__ == "__main__":
  import sys
  import pdb
  import cPickle
  settings.debug=True
  def debugger(type, value, tb):
    pdb.pm()
  sys.excepthook = debugger
  lr = open("lastRequest", "r")
  req = cPickle.loads(lr.read())
  lr.close()
  print bForm(req, 1)
