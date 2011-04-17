"""
  " These routines store data from an Octo Forms into a database. 
  "
  " (c) Charles Shiflett 2010-11
  "
  "
  "" "" "" "" "" "" "" "" "" "" "" "" """

import psycopg2 as db
import psycopg2.pool as dbPool
import bfbdb
import cPickle
import decimal
import settings
import datetime

import logging
log = logging.getLogger('forms.bfsql')
logging.basicConfig(level=logging.DEBUG)

""" 
Functions:

  getForm    ( id, refno ) - retrieve a keyed form from SQL database by ref no
  getNamedForm ( name )    - return id associated with name
  insertForm ( id, data, metaData={} ) - save a keyed form.
  
"""


DB_USAGE = " Could not connect to PostgreSQL Database. See DB INSTALL.  "

try: 
  pool = dbPool.ThreadedConnectionPool(1, 20, \
    "dbname=%s" % settings.BFORMS_DATABASE_NAME)
  #conn = db.connect( """
  #  dbname=%s
  #  """ % settings.BFORMS_DATABASE_NAME )
except:
  raise
  raise ValueError( DB_USAGE + "Configured DB: " + settings.BFORMS_DATABASE_NAME )


def getColData( cur, bdb_id ):
  """ Returns column names associated with a form """
  SQL = """
    SELECT attname FROM pg_catalog.pg_attribute
     WHERE 
      attnum > 0 AND 
      attrelid= (
          SELECT oid FROM pg_catalog.pg_class WHERE relname='bf%s'
        ) 
  ;
  """ % bdb_id; 
    
  cur.execute ( SQL )
  data = cur.fetchall()

  if not data:
    cur.execute ( 
      'CREATE TABLE BF%s ( id SERIAL PRIMARY KEY NOT NULL )' % bdb_id )

  return map( lambda(z): z[0], data )

def getMetadata ( key, limitTables ):
  """Try to retrieve the metadata key from all tables owned by the current user
       - Mostly for accounting information related to all data collected ...

    @return: key, tableId, dateCreated, refNo 
  """
  conn = pool.getconn()
  tableNameSQL = "SELECT tablename FROM pg_tables" \
               + "  WHERE tableowner=(SELECT CURRENT_USER);"
  conn.commit()
  cur = conn.cursor()
  cur.execute ( tableNameSQL ) # Make sure that A. User asked for table
  tableNames  = cur.fetchall() #            and B. Table Exists.
  tableName = ( x[0] for x in tableNames ) 
  filterNames = filter( lambda x: x in limitTables, tableName )

  metaQuery = [ "SELECT %s,'%s', dateCreated, id FROM %s" % (key, name[2:], name) for name in filterNames ] 

  if not len(metaQuery):
    log.debug("metaQuery %s returned no data" % metaQuery)
    cur.close()
    pool.putconn(conn)
    return []

  cur.execute ( " UNION ".join(metaQuery) ) 
  retval = cur.fetchall()
  cur.close()
  pool.putconn(conn)

  return retval


def createColumn ( cur, bdb_id, newMapping, data ):
  # List of conversions between Python types and postgres types
  import datetime
  import decimal

  typeMap = { 
    float             : "float",
    datetime.datetime : "timestamp with time zone", 
    datetime.time     : "time with time zone", 
    datetime.date     : "date", 
    unicode           : "text",
    str               : "text",
    decimal.Decimal   : "decimal",
    list              : "text[]",
    int               : "bigint"
  }


  #print "createColumn () called"
  oldMapping = getColData ( cur, bdb_id )

  if not oldMapping:
    oldMapping=()

  inserts = []
  for item in newMapping.split(","):
    if item.lower() not in oldMapping:
      try: 
        inserts.append (( item, typeMap[ type(data[item]) ] ))
        # Check sub-Items here.
      except Exception, e: 
        log.error("Err (%s) ins DB col, %s %s" % (e, type(data[item]), item) )
        raise ValueError ( "Type %s not found. Can't create DB Column %s." %
          ( type(data[item]), item ) )

        
  inserts.sort()
  for i in inserts:
    sql = "ALTER TABLE bf%s ADD COLUMN %s %s" % (bdb_id, i[0], i[1]) 
    log.debug( "SQL.add.column: %s" % sql )
    cur.execute ( sql )
  
def getForms ( barcode, parent ):   
  "named forms blah blah blah"
  pass
  
  
  
def getForm ( bdb_id, refNo=False, lim="*"):   
  """
  Each form is uniquely keyed by the berkeley Form Id, and the ref. no

  If refNo is False, then return all forms associated with a specific bdb_id.
  
  When you request a form, if bdb_id is a revision, find the base form first. 
   - newMap.sort() changes the order somehow. Probably the original question ordering.
  """
  conn= pool.getconn()
  cur = conn.cursor()

  # Get Mapping.
  bForm = bfbdb.loadObject (bdb_id) 
  newMap, parent = bfbdb.loadMap(bForm)
  newMap.sort()

  if not parent:
    parent = bdb_id

  # Do Select
  try: 
    if refNo: 
      cur.execute("SELECT %s FROM BF%s where id=%d" % (lim,parent,int(refNo)))
      result = cur.fetchall()
    else: 
      # When doing a select *, remember that you are always selecting
      # against the base form. Would be nice to optimize this to take
      # adavantage of named items (which don't currently exist)...
      cur.execute ( "SELECT %s FROM BF%s" % (lim, parent) )
      result = cur.fetchall()
  except db.DatabaseError, e:
    log.debug ( "Error performing select ... Error was %s " % e )
    # conn.rollback() # Don't need to to rollback, no data modified
    cur.close()
    pool.putconn(conn)
    return []

  key = [ x[0] for x in cur.description ]
  resultSet = []
  for r in result: 
    resultSet.append(dict(zip(key, r)))
  cur.close()
  pool.putconn(conn)

  if not resultSet:
    log.debug("Error: Query returned no data. %s/%s" % (bdb_id, refNo) )
    return []

  if refNo:
    # Apply mapping from Berkeley Form object to data retrieved from SQL select
    return dict(mapOld2New( newMap, resultSet[0].items() )[1])
  else:
    return resultSet
def miniPageOrder( x ):
  key = x[0]
  if len(key) < 6:
    return key
  return "%s%s%s" % (key[:4], key[-1], key[4:8])

def mapOld2New( formMap, data, prefix="", postfix="", i=0 ):
  newIds = formMap
  newIds.sort( key=lambda x: x[1] )
  newData = []
  data.sort(key= miniPageOrder)

  while i < len(data):
    if len(prefix) and (data[i][0][-1] != postfix) :
      return i, newData # A more elegant solution would involve using a subset of data
    key, d = data[i]
    try:
      if len(prefix):
        keyNum = int(key[5:8])
        #keyNum = int(key[int(1+len(prefix)):int(4+len(prefix))]), no q
      else:
        keyNum = int(key[1:4])
      fullKey = "%sq%03d%s" % (prefix, int(newIds[keyNum-1][0]), postfix)
    except:
      i+=1
      continue
    if d:
      newData.append( (fullKey, d) )
    if type(newIds[keyNum-1][2]) == type([]):
      i+=1
      try:
        for j in range( int(d) ):  
          i, d = mapOld2New( newIds[keyNum-1][2], data, prefix=fullKey, postfix="%c" % int(0x61+j), i=i )
          newData+=d
      except:
        pass
      i-=1
    i+=1
  return i, newData
      

def mapNewToOld( formMap, data, prefix="", postfix="", i=1 ):
  returnData = []
  if not data:
    log.debug("No Data, not performing mapping procedure")
    return data
  numItems = data.items()
  numItems.sort( key= lambda x: x[0] )
  try:
    numItems = int(numItems[-1][0][1:4])
  except Exception, e:
    log.error("Error determining # of items for %s, err: %s " % (data, e) )
    raise data
  while i <= numItems:
    key = "q%03d" % i
    fullKey = "%s%s%s" % (prefix, key, postfix)
    if not data.has_key(fullKey):
      i+=1
      continue
    value = data[fullKey] 
    intQ  = int(key[1:4]) -1
    textQ = "%sq%03d%s" % (prefix, formMap[intQ][1], postfix)
    returnData.append( (textQ, value) )
    if type(formMap[intQ][2]) == type([]):
      for c in range(int(value)):
        newData = mapNewToOld ( formMap[intQ][2], data, postfix="%c" % (0x61+c), prefix=textQ )
        returnData += newData
    i+=1
  return returnData
  """
    data = map( lambda(z): 
      (( "q%03d" % newMap[ int(z[0][1:4])-1 ][1] , z[1] )), filteredData )
    data = dict(data)
  """
  

def insertForm ( bdb_id, data, recursionCount=0, metaData={}, cur=None, conn=None ):
  """
   @data   = A dict (key, value) of the items we are inserting. key's are in
               the format q001, q002, q003, etc.
   @bdb_id = Berkeley form from which the data is based.

   XXX1: This model is based on append only database's. In this model, you need
         a key of something to determine when new data is being added.
        
   XXX2: We should have some sort of trigger indicating when data has been
         appended which results in the obsoletion of an existing form.
  """

  if recursionCount > 5:
    cur.close()
    pool.putconn(conn)
    raise ValueError("INFINITE LOOP in insertForm. Error creating TABLE?.")
  if not cur:
    conn = pool.getconn()
    cur = conn.cursor()

  original_data = data
  bForm = bfbdb.loadObject (bdb_id) 
  newMap, parent = bfbdb.loadMap(bForm)

  data = mapNewToOld( newMap, data )
    
  filteredData = []
  for key, value in data:
    if value:
      filteredData.append( (key,value) )
  data = dict(filteredData)

  # Convert newID's to oldID's to save in database. 
  metaData["dateCreated"] = datetime.datetime.now()
  data.update(metaData)

  # Do the insert
  insertionId = None
  if cur:
    items = [ keys for keys in data  ] # copies items from data
    item  = ','.join(items)
    value = ')s,%('.join(items)

    try:
      #sql = "INSERT INTO BF%s (%s) values (%%(%s)s) RETURNING id" % (parent, item, value)
      # FOR 8.1
      sql = "INSERT INTO BF%s (%s) values (%%(%s)s) " % (parent, item, value)
      log.debug("SQL.form.insert: |%s| (%s)" % (sql,data) )
      cur.execute ( sql, data )
      # FOR 8.1
      cur.execute ( "SELECT lastval()" )
    except:
      if recursionCount < 5:
        conn.rollback()
        createColumn ( cur, parent, item, data )
        conn.commit()
        return insertForm ( bdb_id, original_data, recursionCount+1, metaData=metaData, cur=cur, conn=conn )
      raise # This raise is redundant with the INFINITE LOOP CHECK above.

    insertionId =  cur.fetchone()[0]
    conn.commit()
    if not insertionId:
      conn.rollback()
      cur.close()
      pool.putconn(conn)
      log.warn("An insert failed, SQL was %s" % locals().get('sql', 'NO SQL') )
      return 1
  else:
    raise ValueError("The connection to our database is broken :(.")

  cur.close()
  pool.putconn(conn)
  return insertionId

def getNamedForm ( name ):
  SQL = "SELECT form FROM form_names where name=%(name)s"
  conn = pool.getconn()
  cur = conn.cursor()

  try:
    cur.execute( SQL, locals() )
    data = cur.fetchone()
  except Exception, e:
    log.debug("form not found (%s) in getNamedForm, err %s" % (name, e))
    data = None

  cur.close()
  pool.putconn(conn)
  return data
  

def insertNamedFormR ( name, form, cur, update=True, count=0 ):
  count += 1
  if count > 7:
    raise ValueError ( "Create table failed in insertNamedFormR" )
 
  if update:
    SQL = "UPDATE form_names SET form=%(form)s WHERE name=%(name)s"
    try:
      cur.execute(SQL, locals() )
      if cur.rowcount:
        return 
    except Exception, e:
      log.debug( "insertNamedFormR falling back on insert %s" % e )
      insertNamedFormR( name, form, cur, update=False, count=count )
      return

  try:
    SQL = "INSERT INTO form_names (name, form) VALUES (%(name)s, %(form)s)"
    cur.execute ( SQL, locals() )
  except:
    log.debug( "form_names table did not exist, trying to create it")
    SQL = "CREATE TABLE form_names (name text, form bigint)"
    cur.execute ( SQL )
    insertNamedFormR( name, form, cur, count=count )

  
def insertNamedFormTest ( name, refno ):
  " Just like InsertNamedForm, but takes different arguments. For testing. "
  conn = pool.getconn()
  cur = conn.cursor()

  try:
    insertNamedFormR ( name, refno, cur )
    conn.commit()
  except Exception, e:
    log.warn(" insertNamedFormTest failed to insert %s %s" % (name, refno) )
    log.warn(e)
    conn.rollback()
    raise

  cur.close()
  pool.putconn(conn)


def insertNamedForm ( name, bdb_id, data, metaData={} ):
  conn = pool.getconn()
  cur = conn.cursor()

  refno = insertForm(bdb_id, data, metaData, cur=cur)
  insertNamedFormR ( name, refno, cur )

  conn.commit()
  cur.close()
  pool.putconn(conn)




