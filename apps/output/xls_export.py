"""
  " (c) Charles Shiflett 2011
  "
  "
  "" "" "" "" "" "" "" "" "" "" "" "" """

import xlwt
from datetime import datetime

import apps.forms.form_models.bfbdb  as bfbdb
import apps.forms.form_models.bform  as beform

import sys

import pdb
    
def debugger(type, value, tb):
  pdb.pm()

sys.excepthook = debugger

BaseFields = [ "questionId", "questionType", "label", "style", "constraints" ]
AddlFields = [ "choices", "oratab", "oracol", "oracom", "oraval" ]

font0 = xlwt.Font()
font0.name = 'Times New Roman'
font0.colour_index = 0 
font0.bold = True

normalSty = xlwt.XFStyle()
normalSty.font = font0

dateSty = xlwt.XFStyle()
dateSty.num_format_str = 'D-MMM-YY'


def recurseQuestions ( bform, ws, rowNum=2 ):
  for question in bform.Questions:
    colNum = 0

    if question.questionType == 1024:
      ws.write(rowNum, 0, question.bForm.myId, normalSty)
      ws.write(rowNum, 1, "MiniPage", normalSty)
      ws.write(rowNum, 2, "StartLoop", normalSty)
      rowNum=recurseQuestions( question.bForm, ws, rowNum+1 )
      ws.write(rowNum, 1, "MiniPage", normalSty)
      ws.write(rowNum, 2, "EndLoop", normalSty)
      rowNum+=1
      continue

    for item in BaseFields:
      # Write one column per form.
      data = getattr(question, item, "")
      if type(data) == type({}):
        data = [ "%s:%s" % ( str(x[0]), str(x[1]) ) for x in data.items() ]
        data = ",".join(data)
      if item == "questionType":
        data = beform.BFORM_TN[ data ]
      ws.write(rowNum, colNum, data, normalSty)
      colNum+=1

    addl = len( getattr(question, "choices", ()))
    orat = len( getattr(question, "oratab", () ))
    if orat > addl:
      addl = orat

    for count in range( addl ):
      if addl > 1:
        rowNum+=1
      colNum=len(BaseFields)
      for item in AddlFields:
        data = getattr(question, item, []) 
        if len(data) > count:
          if item=="choices":
            data = data[count].label
          else:
            data = data[count]
          ws.write(rowNum, colNum, data, normalSty)
        colNum+=1
    rowNum+=1


  return rowNum


def createXLS(file=None, bform=None):
  wb = xlwt.Workbook()
  ws = wb.add_sheet('XLS Export')

  recurseQuestions( bform, ws )

  count=0
  for item in ["bKey", "type", "label", "style", "constraints"] + AddlFields:
    ws.write(0, count, item, normalSty)
    count+=1

  ws.write(1, 0, bform.myId, normalSty)
  ws.write(1, 1, "myId", normalSty)
  wb.save(file)

