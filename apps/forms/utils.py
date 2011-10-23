import gen
import cPickle

"""
  This contains misc. utilities, such as the embedded web server for testing.
    (c) Charles Shiflett 2011


"""

def handleMinipage ( df, data ):
  """
  Adds or removes a page from a minipage.

    * df   = django form
    * data = form data 

  """
  oper = 0
  if df.has_key("miniPageAdd") or df.has_key("miniPageDel"):
    if df.has_key("miniPageAdd"):
      miniNum = df["miniPageAdd"]
      oper = 1
    else:
      miniNum = df["miniPageDel"]
      oper = -1

    try:
      data[miniNum] = int(data[miniNum]) + oper
    except:
      pass

    if data[ miniNum ] < 1:
      data[ miniNum ] = 1
  else:
    return False, False
  return data, miniNum

def spawnServer ():
  import cgi
  import BaseHTTPServer 
  import urlparse

  class HttpHandler(BaseHTTPServer.BaseHTTPRequestHandler):
    def dispatch(self, data=None):
      path = urlparse.urlparse(self.path)
      print "request: ", path
      print "data: ", data
      args = path.path.split("/")
      print "args: ", args
      self.send_response(200)
      self.send_header('Content-Type', 'text/html')
      self.end_headers()
      request = {}
      request['method'] = 'POST' if data else 'GET'
      try:
        d = dict(data)
        request['POST'] = {}
        for key in d.keys():
          # XXX: obviously this has issues with files, and maybe lists.
          request['POST'][key] = d[key].value
      except Exception, e:
        request['POST'] = None


      output = False
      try: 
        if args[1][:4] == 'form':
          lastRequest = open("lastRequest", "w")
          lastRequest.write(cPickle.dumps(request))
          lastRequest.close()
          try: 
            try: 
              output = gen.bForm(request, int(args[2]), refNo=int(args[3]) )
            except: 
              output = gen.bForm(request, int(args[2]) )
          except Exception, e:
            print "Err: ", e, e.__dict__
        if args[1][:4] == 'temp':
          with open ("../../test/html/dojo.html") as f:
            output = f.read()
      except:
        pass

      output = output if output else 'usage: url://host/form/#/'
      self.wfile.write( output )
      return 

    def do_GET(self): 
      return self.dispatch()

    def do_POST(self):
      form = cgi.FieldStorage( 
               fp=self.rfile, 
               headers=self.headers, 
               environ={'REQUEST_METHOD':'POST', 
                        'CONTENT_TYPE':self.headers['Content-Type'], }
             )
      return self.dispatch(form)


  from SocketServer import ThreadingMixIn
  class ThreadingHTTPServer(ThreadingMixIn, BaseHTTPServer.HTTPServer): 
      pass


  server = ThreadingHTTPServer(('localhost', 8080), HttpHandler)
  print "Starting HTTP Server on localhost, 8080"
  while 1:
    server.handle_request()


def listKeys():
  from bsddb import db
  import settings
  db_env = db.DBEnv()

  # Open the Database, use TXN
  # Not supported in BDB 4.5ish. 
  #db_env.open(PROJECT_DATA_ROOT+"/data", db.DB_REGISTER|db.DB_CREATE|db.DB_RECOVER|db.DB_INIT_MPOOL|db.DB_INIT_LOCK|db.DB_INIT_LOG|db.DB_INIT_TXN|db.DB_CHKSUM)
  db_env.open(settings.BDB_PATH, db.DB_CREATE|db.DB_RECOVER|db.DB_INIT_MPOOL|db.DB_INIT_LOCK|db.DB_INIT_LOG|db.DB_INIT_TXN|db.DB_CHKSUM)
  db_env.set_timeout( 16384, db.DB_SET_LOCK_TIMEOUT )
  db_env.set_timeout( 16384, db.DB_SET_TXN_TIMEOUT)
  bdb = db.DB(db_env)
  bdb.open(settings.BDB_NAME, settings.BDB_PATH )

  keys = bdb.keys()
  keys.sort()
  print "Keys:", keys
  bdb.close()
  db_env.close()

 
if __name__ == '__main__':
  import sys
  import pdb 
  def debugger(type, value, tb):
    pdb.pm()
  sys.excepthook = debugger
            
  try: 
    listKeys()
  except:
    pass
  spawnServer()

