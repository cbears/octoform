#!/usr/bin/env python
# encoding: utf-8
""" 
  Detritus. 
  (c) Charles Shiflett 2011 
"""
from django.core.management import setup_environ
import settings
setup_environ(settings)

import os
import xlrd
import sys
import apps.forms.form_models.bform as bforms
import apps.forms.form_models.bfsql as bfsql
from apps.forms.form_models.bfbdb import *

import pdb

def debugger(type, value, tb):
  pdb.pm()

sys.excepthook = debugger 


def getMappings(sheet):
  mapping = {}
  for col in range(sheet.ncols):
    try:
      mapping[sheet.cell_value(rowx=0,colx=col).lower()] = col
    except:
      print "erorr on "+str(col)
      
  return mapping

def initDatarow( listItems ):
  datarow = {}
  for initItems in listItems:
    datarow[initItems] = []
  return datarow

def parseKeyPair( value ):
  # Parse style/constraint attributes
  vs = value.split('|') 
  valdict={}
  for v in vs:
    val = v.split(':', 1) #It's a key-value pair
    try:
        if val[1] == "False":
           val[1] = False
        if val[1] == "True":
           val[1] = True 
        try: 
          if val[1][0] == '{' and val[1][-1] == "}":
            val[1] = eval(val[1])
        except:
          pass
        valdict[val[0]]=val[1]
    except IndexError:
        pass
  return valdict

def I( i ):
  try:
    return int(i)
  except:
    return i
 
def xlsnarf(xlsfile):
    try:
      book = xlrd.open_workbook(xlsfile)
    except:
      raise ValueError("Error reading '%s', are you sure it is an excel file." % xlsfile )
    sheet = book.sheet_by_index(0)
    bform = []
    mappings = getMappings(sheet)
    lastLabel = "2140Shattuck711"
    listItems = ("choices","oratab","oracol","oracom","oraval")
    joinedItems= listItems[-4:]
    label = lastType = type = ""
    datarow=initDatarow(listItems)
    parent=None
    title = "untitled"

    for row in range(sheet.nrows):
      try:
        #skip the header
        #print "row: ", row
        
        comment=False
        if int(row) < 1:
            continue
        #acquire the data
        label = unicode(sheet.cell_value(rowx=row,colx=mappings["label"]))
        type  = unicode(sheet.cell_value(rowx=row,colx=mappings["type"] ))

        if type == "myId":
          parent = I(sheet.cell_value(rowx=row,colx=mappings["bkey"] ))
          continue
          

        if (lastLabel != label) or (lastType != type):
          if label or type:
            if lastLabel != "2140Shattuck711": 
              # Mr. T says "insert foo"
              datarow["xlRow"] = row
              bform.append(datarow)
              datarow=initDatarow(listItems)
            lastLabel = label
            lastType = type

        try:
          if datarow['oraval'][0] == "#":
            datarow.pop('oraval')
        except:
          pass

        for key,colnumber in mappings.items():
            value = unicode(I(sheet.cell_value(rowx=row,colx=colnumber)))
            if key == 'label':
              label=value
            if key == 'type':
              type=value
            if (key == 'choices' and value):
              if value[0] == "{" and value[-1] == "}":
                value = eval(value)
            if (key == 'style') or (key == 'cons') or (key == 'constraints'):
                if key == 'constraints':
                  key = 'cons' # Cons is old name, used for some reason.
                value = parseKeyPair( value )
                if value.has_key('attrs'):
                  datarow['attrs'] = value.pop('attrs')
            if key in listItems:
              if value:
                if isinstance( value, str ): 
                  datarow[key].append(value.strip())
                else:
                  datarow[key].append(value)
            elif value:
              datarow[key] = value
        try: 
          if datarow['type'] == 'Title':
            title=datarow['label']
        except:
          pass
        if len(datarow['oracol']) != len(datarow['oraval']):
          datarow['oraval'].append("")
        if len(datarow['oracol']) != len(datarow['oracom']):
          datarow['oracom'].append("")
        if len(datarow['oracol']) != len(datarow['oratab']):
          raise ValueError("Table count != column count. Row=%d." % row)
      except:
        print datarow
        print "An Error occured on line %d." % row
        raise 

        
    bform.append(datarow) # Insert the last row
    return title,bform, parent
        #process the data entries

if __name__ == "__main__":
  bf   = bforms.BerkeleyForm()
  bf.baseFont='palatino'
  bf.theme=('default',)
  title,data,parent = xlsnarf(sys.argv[-1])
  bf.title=title.split('|br|')[0]

  try:
    bforms.createQuestions(bf,data)
  except:
    print "Error parsing XLS file, on or around XLS row:", bf.Questions[-1].xlRow
    raise

  print saveObject(bf,parent)
  print bf.title
