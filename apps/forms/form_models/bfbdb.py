"""
  " These routines store the actual form into a database and performs
  " revisioning between form versions.
  "  (c) Charles Shiflett 2010-11
  "
  "" "" "" "" "" "" "" "" "" "" "" "" """

from bsddb import db
#from django.conf import settings
#from forms.form_models.bform import FormChoiceGroup
"""

:method:`mapper`

"""
import os
import cPickle
import settings

import logging
log = logging.getLogger('forms.bfbdb')
logging.basicConfig(level=logging.INFO)
import threading

PROJECT_DATA_ROOT = settings.BDB_PATH
FORMS_DB = settings.BDB_NAME
TEMP_DB  = "%s_temp" % settings.BDB_NAME 

def getDbEnv():
  tl = threading.local() 
  if not hasattr( tl, 'db_env' ):
    tl.db_env= db.DBEnv()
    tl.db_env.open( PROJECT_DATA_ROOT, 
      db.DB_INIT_MPOOL|db.DB_INIT_LOCK|db.DB_INIT_LOG|db.DB_REGISTER|
      db.DB_RECOVER|db.DB_INIT_TXN|db.DB_CHKSUM|db.DB_THREAD|db.DB_CREATE )
    #Use the following if you get errors about db.DB_REGISTER
    #tl.db_env.open( PROJECT_DATA_ROOT, 
    #  db.DB_INIT_MPOOL|db.DB_INIT_LOCK|db.DB_INIT_LOG|
    #  db.DB_INIT_TXN|db.DB_CHKSUM|db.DB_THREAD|db.DB_CREATE )
    tl.db_env.set_timeout( 16384, db.DB_SET_LOCK_TIMEOUT )
    tl.db_env.set_timeout( 16384, db.DB_SET_TXN_TIMEOUT  )
  return tl.db_env

def mapper( newObject, txn=None, bdb=None ):
  """ 
  mapper maps between revisions of a form. We are interested in two types of
  maps, those that involve a re-ordering of questions and those that involve
  additional question. 

  * In the case of a re-ordering, our logical parent remains the logical parent
    of our technical parent.

  * If a question addition occurs, we mark ourself as dirty, and children of
    this form will mark this form as their logical parent.  In the future,
    we might want to always map to parent form. We don't currently as it
    simplifies creating the initial map(s). You may need a special case
    to handle deletions correctly when mapping to the parent form. 

  Each form has two parents, technicalParent and logicalParent. The
  technicalParent is the form we are derived from, logicalParent is the
  last form with equal questions
  """

  if not newObject.technicalParent:
    log.info("mapper: called with parent-less object as argument")
    return None

  try:
    oldObject = loadObject( newObject.technicalParent, txn=txn, bdb=bdb )
  except:
    log.error("Tried to load an object, but I was passed a bogus form ID")
    return None

  oldItemIndex = oldObject.getMapping()
  additionalQuestions=False

  parent = oldObject.logicalParent

  if not parent:
    parent = newObject.technicalParent

  if oldObject.isDirty:
    parent = newObject.technicalParent

  for newItem in newObject.getMapping():
    if newItem not in oldItemIndex:
      additionalQuestions=True

  if not additionalQuestions:
    oldObject = loadObject( oldObject.logicalParent, txn=txn, bdb=bdb )
  else:
    newObject.isDirty = True
    

  # At this point, we are ready to do the mapping between the two objects.
  newDict = newObject.getMapping()
  oldDict = oldObject.getMapping()

  map = []
  for dbId, itemNumber in newDict.items():
    if oldDict.has_key(dbId):
      map.append ( (itemNumber, oldDict[ dbId ]) )
    else:
      map.append ( (itemNumber, None) )

  map.sort()
  newObject.mapping = map

  return parent

def loadMap (bForm, recursionLevel=0, bailEarly=False):
  """ loadMap recursively loads a mapping from this form to a base form 
  
  Our mapping is always a list of ( newItem, oldItem ), something like:
    [( 1, 7 ), (2, 4), (3, -)]

  loadMap converts question mapping to a three tiered map
  
  New      Orig    Db Id    
  _____    _____   _____  
  1        7       1234
  2        4       2345
  3        10      2222


  Where 10 would be created. It would be ++ (size of list).

  returns: map, original form
  """
  if recursionLevel > 256:
    raise ValueError ("We might be in an infinite loop (loadMap). Aborting.") 

  parent = questionMap = None

  try: 
    if bForm.logicalParent != bForm.myId: 
      questionMap, parent = loadMap ( loadObject(bForm.logicalParent), recursionLevel+1 )
  except:
    log.warning("Warning: missing logicalParent in loadMap () ")

  bMap = bForm.getMapping()
  if questionMap == None: 
    #no mapping return no mapping case.
    returnList = []
    for questionId, item in bMap.items():
      returnList.append ( (item, item, questionId ) )
    returnList.sort()
    parent=bForm.myId
  else:
    oldItems     =  map( lambda(z): z[1], questionMap )
    questionMap =  map( lambda(z): (None, z[1], z[2]), questionMap )

    for newItem, oldItem in bForm.mapping:
      if oldItem in oldItems:
        questionMap[oldItem-1] = ( newItem, questionMap[oldItem-1][1], questionMap[oldItem-1][2] )
      else:
        #QA: Are deleted items brought back to life correctly.
        newItemNumber = len ( questionMap ) + 1
        newId = None
        for questionId, item in bMap.items():
          if item == newItem:
            newId = questionId

        if not newId:
          raise ValueError("Assert: newId == None, (not found in question map)")

        questionMap.append( (newItem,  newItemNumber, newId) )

    questionMap.sort()  
    returnList = []

    #Move un-mapped items to the end of the list ( Should implement custom sort )
    j=0
    for newItem, abba, zabba in questionMap:
      if newItem:
        returnList.append(questionMap[j])
      j+=1

    j=0
    for newItem, abba, zabba in questionMap:
      if not newItem:
        returnList.append(questionMap[j])
      j+=1
  
  if bailEarly:
    return returnList, parent

  # Do mapping for minipages as well. Can add recursion to support depth > 2.
  i=0
  for new_id, old_id, key in returnList:
    try:
      if key[0] == "m":
        # Minipage ID's are denoted by 'm', followed by bform id of minipage
        bForm = loadObject (key[1:]) 
        miniMap, miniParent = loadMap(bForm)
        miniMap.sort
        returnList[i] = (new_id, old_id, miniMap)
    except:
      pass
    i+=1

  return returnList, parent

def saveTempObject(bForm, key):
  isSaved=True
  db_env = getDbEnv()
  bdb = db.DB(db_env)

  try:
    txn = db_env.txn_begin() 
    bdb.open(TEMP_DB, PROJECT_DATA_ROOT,  flags=db.DB_CREATE, 
             dbtype=db.DB_BTREE, txn=txn ) 
    bdb.put(key, cPickle.dumps(bForm,2), txn=txn )
  except:
    txn.abort()
    isSaved=False
  txn.commit()

  # CLOSE
  bdb.close()
  return isSaved

def loadTempObject(key, bdb=None):
  setClose=False
  if not key:
    log.warning("loadTempObject called without key")
    return None, None

  if not bdb:
    db_env = getDbEnv()
    bdb = db.DB(db_env)
    bdb.open(TEMP_DB,PROJECT_DATA_ROOT, dbtype=db.DB_BTREE, txn=txn )
    setClose=True

  bdb_data = bdb.get(key, txn=txn)

  # CLOSE
  if setClose:
    bdb.close()

  if (bdb_data):
    return cPickle.loads(bdb_data)
  else:
    log.error("Could not unpickle (temp) data contained with key %s" %  key)
    raise ValueError ("Could not unpickle temp contained with key %s "% key)

#saveObject needs to be called first, to create a database. 
def saveObject(bForm, parent=None):
  """ saveObject does the following:

      *  It serializes python objects and stores them to a berkeleyDB using TXN
      *  It stores an exact copy of the form data from a SQL DB at obj creation
      *  It stores markup, which affects how objects are rendered
      *  It maps newer revisions to older revisions of a form
      *  It stores a revision history 

      @bForm   = the Berkeley Form to be saved
      @parent  = the prior revision ( no circular references! )
      
      returns: the newly generated key.

  """
  db_env = getDbEnv()
  bdb = db.DB(db_env)

  # TXN 
  try:
    txn = db_env.txn_begin() 
    bdb.open(FORMS_DB, PROJECT_DATA_ROOT,  flags=db.DB_CREATE, 
             dbtype=db.DB_BTREE, txn=txn ) 
    # TXN can not be re-used thus we re-open every time. If speed is an
    # issue, we can come up with an alternate approach.

    # Find the last record. 
    cursor = bdb.cursor(txn=txn)
  
    if cursor.last(): 
      key = int(cursor.last()[0]) + 1 
    else:
      key = 1
      log.info("We are (hopefully) starting a new DB, Key=1.")
    bForm.myId = bForm.technicalParent = bForm.logicalParent = key

    key = "%020d" % (key) # Store key as string to ensure consistent sort order

    if (parent):
      # create a mapping between this bForm and appropriate parent
      log.debug("Saving as a revision to %s" % parent)
      bForm.technicalParent = parent
      bForm.logicalParent   = mapper ( bForm, txn, bdb ) 

    if bForm.myId == bForm.technicalParent == bForm.logicalParent:
      log.debug("We are creating/modifying a new form")

    log.debug ("writing %s" % (key) )

    cursor.close()

    bdb.put(key, cPickle.dumps(bForm,2), txn=txn )
  except:
    txn.abort()
    raise
  txn.commit()

  # CLOSE
  bdb.close()
  return int(key)

def loadObject(key, txn=None, bdb=None):
  """
  This method loads a bfbdb object with a particular key
  For example:
  >>> print loadObject(2)
  """

  if not key:
    log.warning("loadObject called without object id")
    return None, None


  key = "%020d" % (int(key))
  setClose=False

  #Debug: 
  #print "reading %s" % (key)

  # OPEN 
  if not bdb:
    db_env = getDbEnv()
    bdb = db.DB(db_env)
    bdb.open(FORMS_DB,PROJECT_DATA_ROOT, dbtype=db.DB_BTREE, txn=txn )
    setClose=True

  bdb_data = bdb.get(key, txn=txn)

  # CLOSE
  if setClose:
    bdb.close()

  if (bdb_data):
    return cPickle.loads(bdb_data)
  else:
    # Need to return an error.
    raise ValueError ("Tried to load form %d, which has no data"% int(key) )

def loadChoiceGroups(owner=None, txn=None, bdb=None):
  """
  XXX: Not used anymore?
  """
  setClose=False
  if not bdb:
    db_env = getDbEnv() 
    bdb = db.DB(db_env)
    bdb.open(FORMS_DB,PROJECT_DATA_ROOT, dbtype=db.DB_BTREE, txn=txn )
    setClose=True
  bdb_keys=bdb.keys()
  choice_groups = []
  if setClose:
    bdb.close()
  for bdb_key in bdb_keys:
    d = bdb.get(bdb_key,txn=txn)
    bdb_data = cPickle.loads(d)
  
  """
    if type(bdb_data) == FormChoiceGroup:
      print "type was FormChoiceGroup!"
      if setClose:
        bdb.close()
        db_env.close()
      if bdb_data:
        choice_groups.append(bdb_data)
      else:
        # Need to return an error.
        raise ValueError ("Tried to load ChoiceGroup %d, which has no data"% int(bdb_key) )
  """
  return choice_groups
#Code for testing.
#

#for y in range(8, 12):
#  newQuestions = []
#   for i in range(1,11):
#     newQuestion = {}
#     newQuestion['type']   = "Multi_Single"
#     newQuestion['id']     = 12345+i
#     newQuestion['label']  = "Barbaric %d" % (i)
#     newQuestion['db_id']  = i*i*i
#     newChoices=[]
#     for j in range(1,4):
#      newChoices.append((j,"%d %d" % (i, j) ))
#    newQuestion['choices'] = newChoices
#    newQuestions.append(newQuestion)
#  #Form created... Save form
#  #print newQuestions
#  saveObject( newQuestions )
#
##print loadObject(4)
#print get_map(loadObject(2))
#
#print db.version()
#
#
##class myTestObject:
##  field1="ABRA CADABRA"
##  field2=( "ONE", "TWO", "THREE" )
##  field3={ "bar":"one", "ram":"truck" }
##
##newObject = myTestObject()
##
#
#for i in range( 0, 512):
#  saveObject  ( newObject, parent="fortyu" )
#
#for i in range( 420, 1, -1 ):
#   print loadObject( i )
  
