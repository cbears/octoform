""" 
  Detritus. 
  (c) Charles Shiflett 2011 
"""
import os.path
import apps.forms.form_models.bform as bforms
import xlsnarf
import xlrd
from apps.forms.form_models.bfbdb import *
from apps.forms.inventory.models import *
from django.conf import settings

import pdb
debug=True
def listXLSFiles(directory):
  dirlist = os.listdir(directory)
  flist = []
  print os.path.abspath(directory)
  for dir in dirlist:
   if (str(dir) != ".svn") & (dir != 'README'):#check for isdir instead of fname 
    files = os.listdir(directory+'/'+dir)
    for file in files:
      if (str(file).endswith('xls')):
        flist.append(os.path.abspath(directory)+"/"+dir+'/'+file)
  return flist 

def snarfFile(fname,code=False):
  print "beginning the processing of:"+fname
  title,data,parent=xlsnarf.xlsnarf(fname)  
  title = title.split('|br|')[0] #for multi-line titles, only take the first line
  bf = bforms.BerkeleyForm()
  bf.baseFont='palatino'
  bf.theme=('default',)
  try:
    bforms.createQuestions(bf,data)
  except:
    print data
    print "An error occured with file:"+fname
    print "this is mostly likely a transaction error "
    return

  bfbdbid=saveObject(bf,parent)
  print bfbdbid
  if code== False:
    return [title,bfbdbid]
  else:
    m = InventoryMapping()
    m.code=code[:2]
    m.title=title
    m.pages=1
    m.bfbdbid=bfbdbid
    m.save()


def snarfFiles(files):
  major, minor, revision = xlrd.__VERSION__.split(".")
  if (int(minor) < 7) and (int(major) < 1):
    print "Warning, Expected XLRD >= 0.7 "
    print "XLsnarf using XLRD version %s " %  xlrd.__VERSION__
  pids={}
  for file in files:
    print file.split("/")[-2]
    snarfFile(str(file),file.split("/")[-2])
"""
>>> files = listXLSFiles(settings.MEDIA_ROOT+'mapping/final')
>>> snarfFiles(settings.MEDIA_ROOT+'mapping/final/',files)
"""
