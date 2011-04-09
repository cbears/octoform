import forms.form_models.bform as bforms
import forms.form_models.bfbdb as bdb
import forms.form_models.bfsql as bfsql
import forms.form_models.templateLoader as templateLoader

import pdb
import sys

def debugger(type, value, tb):
  pdb.pm()

sys.excepthook = debugger

def testCreateQuestion():
  bf= bforms.BerkeleyForm ( )

  bf.Questions.append( 
    bforms.createQuestion ( 
      "CheckMany", 
      "Lame Question?", 
      ("Yes","No","Maybe."), 
      ("useless", "questions")  
    ) 
  )

  bf.Questions.append( 
    bforms.createQuestion ( 
      "Text", 
      "Test Sub Items", 
      subItems=( ("Text", "Foo"), ("Text", "Bar"), ("Text", "Baz") )
    )
  )

  bf.Questions.append( 
    bforms.createQuestion ( 
      "Text", 
      "Simple"
    )
  );

  bfNum = bdb.saveObject (bf) 
  #print "Create Question Form Id= ", bfNum
  loaded = bdb.loadObject(bfNum)
  bformData = bforms.bformData( loaded, {u'q003': [u'sadlk'], u'q002': [u'aslkdj'], u'q001': [u'c000', u'c001'], 'q002_1': 'bar', 'q002_2': 'foo', 'q002_3': 'baz'} )
  if bformData.is_valid(): 
    refNo = bfsql.insertForm( bfNum, filledDjangoForm.getData() )
  else:
    print unicode(filledDjangoForm._errors)

"""
SPEED TESTS:
  time python thisfilename.py
  1024 / number of seconds = num. loads/ s
  Sun Jul  5 12:28:35 PDT 2009 == 188 on 1.2Ghz laptop

for i in xrange(1, 1024):
  if (i & 255) == 255:
    print i, "."
  bdb.loadObject(4)
"""



def testFormCreation():
  id_list = [ 1, 2, 3, 4, 5, 6, 5, 6, 4, 1, 7, 8, 8, 6, 9, 1, 10, 11 ]

  # PROGRAMATICALLY CREATE FORMS.
  formList = []
  j = 0
  for i in xrange( 1, 4 ):
    bf= bforms.BerkeleyForm ( )
    fq = bforms.FormQuestion  \
      (-1, bforms.BFORM_TYPE["Section"], "Section One")
    bf.Questions.append(fq)
    k=0
    for name in ("Alpha", "Beta", "Gamma", "Delta", "Epsilion", "Zeta"):
      fq = bforms.FormQuestion  \
              (id_list[j], bforms.BFORM_TYPE["Text"], "%s %d" % (name, i))
      bf.Questions.append(fq)
      j+=1
      k+=1

    fq = bforms.FormQuestion  \
      (-1, bforms.BFORM_TYPE["CloseTag"], "End Section One")
    bf.Questions.append(fq)

    formList.append(bf)

  # SAVE THEM 
  formId = []
  lastId = None
  for form in formList:
    lastId = bdb.saveObject( form, parent=lastId )
    formId.append( lastId )

  # SUBMIT DATA WITH THEM 
  refNumbers = []
  formId.sort(reverse=True)
  x = 0
  for id in formId:
    bForm = bdb.loadObject ( id ) 
    #djangoForm = templateLoader.makeForm( bForm, None )
    bformData = bforms.bformData ( bForm, {} )

    for j in xrange(1, 5):
      i = 0
      for name in ("Aleph", "Beis", "Gimel", "Daled", "Heh", "Vov"):
        i+=1
        x+=1
        bformData["q%03d" % i] = "%s (% 2d-% 3d)" % (name, j, x)

      if bformData.is_valid(): 
        #print "Trying insert on ", id
        refNo = bfsql.insertForm( id, bformData.getData() )
        bfsql.insertNamedFormTest ( "ABBA%d" % refNo, refNo )
        if not refNo:
          print "Form insert == bad. Bummer."
        else:
          refNumbers.append((refNo, id))
          
      else:
        print "ERROR: ", djangoData


  # LOAD THE SAVED
  i=0
  for refNo, id in refNumbers:
    form = bfsql.getForm( id, refNo )
    # do some magic to get it into old style format.
    form = form.items()
    form.sort( key= lambda x: x[0] )
    form = [ x[1] for x in form if x[0].startswith("q") and x[1] ]
    #form.sort( key= lambda x: x.split("(")[1]  ) 
    try: 
      print " | ".join(form)
    except:
      print form
      print "Error trying to print form contents"



testFormCreation()
#testCreateQuestion()
