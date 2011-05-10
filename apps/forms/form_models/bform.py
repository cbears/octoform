# -*- coding: utf-8 -*-

"""
  " Basic form structure used by octoforms.
  "  (c) Charles Shiflett 2009-11
  " 
  "
  "" "" "" "" "" "" "" "" "" "" "" "" """

from mako.lookup import TemplateLookup
import datetime
import  settings
import bfbdb

import logging
log = logging.getLogger('forms.bform')


""" 
Octo Forms are an object containing a list of python objects.

 * The type of object determines how the object is interpreted by output
filters ( Display to HTML, TEX, ... ).
 * Questions have a type below 256
 * Above 255 is reserved for non question objects ( section headers, etc )
"""  
BFORM_TYPE = {
  "CheckOne":     1, 
  "CheckMany":    3,
  "Text":         4,
  "Time":        16,
  "Date":        18,
  "DateTime":    17,
  "Decimal":     32,
  "Float":       33,
  "TextArea":    34,
  "File":        35, # todo
  "Section":    256,
  "CloseTag":   257,
  "Link":       258, # todo, has special meaning.
  'Info':       260,
  'MiniPage':  1024,
  'Hidden':    1025,
}

class bformData(dict):
  """
  This is for storing form data. We provide a few convenience functions to
  assist in parsing form data and handling data. It is very loosely based
  on Django's form dictionary.
  
    isValid(): Checks to see if data passes validation criteria.
    errors():  Returns errors associated with a form.

  XXX: Lies....
  
  """
  def __init__(self, bdb, d=False):
    if d:
      super(bformData, self).__init__(d)
    else:
      super(bformData, self).__init__()
    self.bdb = bdb
    self['_initialized'] = True

  def is_valid(self):
    return True

  def isValid(self):
    return self.is_valid(self)

  def errors(self):
    return False

  def getData(self):
    " go through self.items(), and return everything with id_, stripping id_ "
    return dict(( (x[0][3:], x[1]) for x in self.items() if x[0][:4]=='id_q' ))




"BFORM_TN is the reverse map of BFORM_TYPE. TN stands for taming name?"
BFORM_TN = dict(map ( lambda(z): (z[1], z[0]), BFORM_TYPE.items() ))

class BerkeleyForm ( object ):
  """
  
  """
  def __init__ ( self ):
    self.technicalParent  = None
    self.logicalParent    = None
    self.myId          = None   # BDB Id 
    self.createdOn    = datetime.datetime.now()    
    self.isDirty      = False
    self.Questions    = []
    self.title        = 'untitled'

  
  def getMapping ( self ):
    """ 
    Returns a dictionary mapping between database Id's and item #'s. 
    """
    
    i=0
    questionMap = {}
    for q in self.Questions:
      if q.questionType == 1024 or q.isQuestion():
        i+=1
      if q.questionType == 1024:
        questionMap["m%d" % q.bForm.technicalParent] = i
      if q.isQuestion():
        if questionMap.has_key(q.questionId):
          log.info("Danger: Duplicate database Id in map. NOT SUPPORTED")
          raise ValueError ("Found a dup DB Id in map... Abort. Retry. Fail.")
        questionMap[str(q.questionId)] = long(i)
    return questionMap

class FormQuestion ( object ):
  """

  """
  def __init__ ( self, questionId, questionType, label, style = None ):
    self.questionId   = questionId
    self.questionType = questionType
    try:
      self.label        = unicode(label, "utf-8", errors='replace')
    except TypeError:
      self.label        = label
    self.choices      = []
    
    # These should all be defined somewhere else like createQ
    self.choicegroup    = None
    self.style        = style
    
    #self.subItems     = False
    """ NO MORE SUB ITEM SUPPORT ... 
    
        We don't really know how to alphabetize sub items in the database, 
        so we either default to _a, _b etc, or we take extensions from ...
    """
    #self.subExtensions = {} # NOT IMPLEMENTED
    # self.subStyle      = provide hints on how to display an object.
    # end move notes

  def isQuestion ( self ):
    """
    """
    if self.questionType < 256:
      return True
    return False
  
  def addChoice (self, choice):
    """
    """
    if type(choice) == FormChoiceGroup:
      self.choices=[] # Redundant ? 
      self.choices.extend(choice.choices)
      self.choicegroup = choice
    if type(choice) == FormChoice:
      self.choices.append ( choice )
    
  def getChoices ( self ):
    """
    """
    newChoices = []
    start = 0;
    for c in self.choices:
      newChoices.append(( "c%03d" % start, c.label))
      start+=1
    return tuple(newChoices)
  def getChoiceGroup( self ):
    return self.choicegroup
    
class FormChoiceGroup( object ):
  def __init__ ( self, choiceGroupId,formChoices = [], ownerId = None, label = None ):
    """ assumes formChoices isn't actually a list of FormChoice objects but rather a list of strings """
    self.choiceGroupId = choiceGroupId
    self.choices = []
    self.ownerId = ownerId
    self.label = label
    if type( formChoices[0] == str ):
      i=0
      for choice in formChoices:
        self.choices.append( FormChoice ( i, choice ) )
        i=i+1

class FormChoice ( object ):
  def __init__ ( self, choiceId, label ):
    self.choiceId = choiceId
    self.label    = label

"Use alternative syntax to prevent a name space collision."
KeyMap = { 
  "type":      "qType",
  "choices":  "qChoices",
  "label":    "qLabel",
  "tags":      "qTags",
  "style":    "qStyle",
  "subitems":  "subItems",
  "cons":      "qConstraints",
}

def keyMap ( val ):
  try:
    return KeyMap[val]
  except KeyError:
    return val

loadedTemplates = {}

def updateAttrs( q ):
  defaults = {}
  if q.questionType==BFORM_TYPE['TextArea']:
    defaults={ 'cols':80, 'style':'font-family:monospace' }
  try:
    defaults.update(q.attrs)
    q.attrs=defaults
  except:
    q.attrs=defaults
    


def dConstrain( question ):
  """
  returns a dictionary of django constraints for the given question

  Note: We could make this two pass: i.e. min_length makes sense for text string
        but not for integer. 
  """

  cMap = { 
    "min":      "min_length",
     "max":      "max_length",
    "null":      "null",
    "editable":    "editable",
    "required":    "required"
  }

  # RegEx constraints should be through non-existant regEx field type.

  if getattr ( question, "constraints", False ):
    return dict( ( ( str(x[0]), x[1] ) for x in getattr ( question, "constraints", False ).items() ) )

  return {"required": False}
  
"""
Helper Functions. May not neccesarily be that helpful.
"""

def createDictQuestion(keys):
  """ 
  This maps between the weird variable names in createQuestion, and the
  normal-ish variable names we use in form creation.
  """
  return createQuestion(**dict(  
    map ( lambda(z): (keyMap(str(z[0])), z[1]), keys.items() ) 
  ) )
  
def createQuestions(bf,questions):
  qNum=0
  while qNum < len(questions):
    if questions[qNum].get("type",False) == "MiniPage":
      if questions[qNum]["label"].lower() == "startloop":
        "The minipage is essentially a standard berkeley form that is"
        "attached to a question. It is recursively defined"
        newForm= BerkeleyForm()
        newForm.baseFont = bf.baseFont
        newForm.theme = bf.theme

        qNum += createQuestions(newForm, questions[qNum+1:])
        if type(2) != type(qNum):
          raise ValueError("Tried to start minipage, but no endLoop found.")

        formNumber=bfbdb.saveObject(newForm, parent=getattr(questions, "bkey",None))
        fq = FormQuestion ( 1, BFORM_TYPE["MiniPage"], "%d" % formNumber, {})
        fq.bForm=newForm
        bf.Questions.append(fq)
      elif questions[qNum]["label"].lower() == "endloop":
        return qNum+1
        
    else:
      bf.Questions.append(
        createDictQuestion(questions[qNum])
      )
    qNum += 1


def createQuestion ( 
  qType   = "Text", 
  qLabel  = "", 
  qChoices= False, 
  qTags   = False, 
  subItems= False, 
  qStyle  = None, 
  qConstraints=None, 
  bkey    = False,
  key=0, 
  **kwargs):

  """
  createQuestions is a helper function to Bforms Init method. It tries to be a
  little smarter about generating errors, coming up with a questionId (If you
  don't happen to already have one), and automatically adds choices.

  qChoices should be an array of strings.

  subItems are complicated. Right now, they are just passed in as a list.
  That list is then re-fed through to createQuestion, which creates the
  sub-item. Rendering them correctly requires template support, which may
  or may not exist.
  """
  if not qType:
    raise ValueError ( "createQuestion called with Null Type or Label" )
  
  isValid = False
  for english, bformish in BFORM_TYPE.items():
    if qType == english:
      isValid = True

  if isinstance( qType, basestring ): 
    qType = BFORM_TYPE[qType]
  
  if not isValid:
    raise ValueError ( "qType (%s) is not in range of supported types"% qType )

  if (qType > 255): 
    # This is markup, it doesn't have real data associated with it, 
    # so we handle it as a special case.
    fq = FormQuestion ( 1, qType, qLabel, qStyle)
    i = 0
    if qChoices:
       for qChoice in qChoices:
         i+=1
         if type(qChoice) == type({}):
           fc = FormChoice(i, qChoice["label"])
           fc.direction = qChoice["direction"]
         else:
           fc = FormChoice(i, qChoice)
         try:
           fc = ( fc[0], unicode(fc[1], "utf-8", errors='replace') )
         except:
           pass
         log.debug("Created question. Label=%s" % fc )
         fq.choices.append(fc)
    for key, val in kwargs.items():
      if val:
        setattr(fq, key, val)
    return fq

    bkey = dBQuestion.id
  else:
    pass

  # Assemble the question
  fq = FormQuestion ( bkey, qType, qLabel, qStyle)

  for key, val in kwargs.items():
    if val:
      setattr(fq, key, val)

  if (qType & 0xfffd) == BFORM_TYPE["CheckOne"]: 
    i = 0
    if qChoices:
      for qChoice in qChoices:
        i+=1
        if type(qChoice) == type({}):
          fc = FormChoice(i, qChoice["label"])
          fc.direction = qChoice["direction"]
        else:
          fc = FormChoice(i, qChoice)
        try:
          fc = ( fc[0], unicode(fc[1], "utf-8", errors='replace') )
        except:
          pass
        fq.choices.append(fc)
    else:
      log.info("Warning: Multi Choice called with no choices")
  if qConstraints:
    fq.constraints = qConstraints
        
  return fq

