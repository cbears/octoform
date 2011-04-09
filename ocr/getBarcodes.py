# -*- coding: utf-8 -*-
"""
Barcode Spider
  (c) Charles Shiflett 2011
"""
import os
import re
import pickle
import optparse

import com.google.zxing.MultiFormatReader;
import javax.imageio.ImageIO;

import com.google.zxing.client.j2se.BufferedImageLuminanceSource as LuminanceSource
import com.google.zxing.BinaryBitmap as BinaryBitmap
import com.google.zxing.common.GlobalHistogramBinarizer as GlobalHistogramBinarizer

import thread
import time




q = re.compile('[0-9]{4}-[0-9]{3}.barcode[.a-z]*png')

class pickleStorage:
  def __init__(s):
    s.stor= {}
  def add( self, index, key ):
    project, page = index.split("-", 1)
    page, extension = page.split(".", 1)
    if not self.stor.has_key(project):
      self.stor[project] = []
    if not ((page, key) in self.stor[project]):
      self.stor[project].append( (page, key) )
  def difference( self, diff ):
    differences = {}
    for key, value in self.stor.items():
      if not diff.stor.has_key(key):
        print "Diff does not have key %s" % key 
      differences[key] = []
      pageList = [ x[0] for x in self.stor[key] ]
      for page,file in diff.stor[key]:
        if page not in pageList:
          differences[key].append( (page, file) )
    return differences

        
      

stor = pickleStorage()
rejects = pickleStorage()

zxCounter=1000
threadCount=0
def doZX(file, index):
  global zxCounter
  global threadCount
  zxCounter+=1 
  t = index.split("-",1)
  x = t[1].split(".")
  rejects.add( index, "%s/%s-%s.barcode.pre.png" % (t[0],t[0],x[0]) )
  try:
    image = javax.imageio.ImageIO.read(file)
    decoder = com.google.zxing.MultiFormatReader()

    source = LuminanceSource(image)
    bitmap = BinaryBitmap(GlobalHistogramBinarizer(source))

    res = decoder.decode(bitmap)
  except:
    threadCount-=1
    return
  code = res.getText()
  stor.add( index, code )
    
  print "ZX: ", index, code
  threadCount-=1


def walkDirectories():
  global threadCount
  for root_dir, directories, files in os.walk("."):
    if root_dir==".":
      continue
  
    for file in files:
      if q.match(file):
        f = open ( "%s/%s" % (root_dir,file) , mode="r" )

        threadCount+=1
        while threadCount > 10:
          time.sleep(.001)
        # Try except blocks are ignored (for obvious reasons) while in thread
        thread.start_new_thread ( doZX, ( f, file ) )

def initArgs():
  parser = optparse.OptionParser("%prog [options] <no argument will scan directory, otherwise file to decode> ")
  parser.add_option("-f", "--file", dest="filename",
    help="write pickle to FILE (Defaults to python.pickle)", 
    metavar="FILE", default="python.pickle")

  return parser.parse_args()

options, args = initArgs()

if args:
  for file in args:
    f = open ( "%s" % (file) , mode="r" )
    doZX( f, file )
else:
  walkDirectories()

file = open (options.filename, "w")
pickle.dump(stor.stor, file)
file.close()

d = stor.difference(rejects)
import zipfile

z = zipfile.ZipFile( "rejects.zip", "w" )

for keys, items in d.items():
  for page, file in items:
    z.write( file )

z.close()
print "Conversion finished. rejects.zip contains barcodes which converted incorrectly."


