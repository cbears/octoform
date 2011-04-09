#!/usr/bin/python
# -*- coding: utf-8 -*-

"""

  Code128 Barcode Detection & Analysis 
    (c) Charles Shiflett 2011

  Finds Code128 barcodes in documents scanned in Grayscale at 300 dpi.

  Usage: 

  Each page of the PDF must be converted to a grayscale PNG image, and should
  be ordered as follows:

    1001/1001-001.png
    1001/1001-002.png
    1001/1001-003.png
    .
    .
    .
    1099/1099-001.png
    1099/1099-002.png

  This program will find & enhance barcodes in those pages, and save it's
  progress to a file of the same name, except with an extension of barcode.png.

"""
DEBUG=False

from PIL import Image
from PIL import ImageOps
import PIL.ImageDraw as draw
from glob import glob
import os
import re

import pdb
import sys

import numpy 
import scipy.signal as ss
import math
import scipy.ndimage.interpolation
import scipy.weave

import logging
log = logging.getLogger('findBarcodes')
if DEBUG:
  logging.basicConfig(level=logging.DEBUG)
else:
  logging.basicConfig(level=logging.INFO)

import filter
unAliasFilter = numpy.array( [ [ 0, 1, 0], [1, 4, 1], [ 0, 1, 0] ], numpy.int )

if DEBUG:
  def debugger(type, value, tb):
    pdb.pm()

  sys.excepthook = debugger
  sys.setrecursionlimit(32768)

filWidth=  102 # / 25
filHeight= 110 # / 30

def calcBarLength(length):
  if length < 6:
    return 1
  elif length < 10:
    return 2
  elif length < 13:
    return 3
  else:
    return 4

def convolve( im, filt, reshape ):
  height, stride = im.shape
  fh,fw = filt.shape
  im    = im.reshape( height * stride )
  filt  = filt.reshape( fh*fw )
  newIm = numpy.zeros ( (height * stride), numpy.int )
  code  = """
  int sum=0, pos;
  int ys=0, fys=0;
  for (int y=0; y < (height-(fh/2)); y++) {
    for (int x=0; x < (stride-(fw/2)); x++) {
      fys=sum=0;
      pos=ys+x;

      int th = ((height-y) < fh ) ? height-y : fh;
      int tw = ((stride-x) < fw ) ? stride-x : fw;

      for (int fy=0; fy < th; fy++) {
        for (int fx=0; fx < tw; fx++) {
          sum+=im[pos+fx]*filt[fys+fx];
        }
        fys+=fw;
        pos+=stride;
      }
      newIm[ys+x] = sum;
    }
    ys+=stride;
  }
  """
  scipy.weave.inline(code,['height','stride','fh','fw','im','filt','newIm'])

  if reshape:
    return newIm.reshape(height,stride )
  else:
    return newIm

  

class barImage (object): 

  def __init__ ( self, im ):
    self.im = numpy.array ( im.getdata() )
    self.stride, self.height = im.size
    self.im = self.im.reshape(self.height,self.stride)
    # Note: im is indexed as [y][x] not...

  def printImg( self, l=[], offset=0):
    l = [ (i[1], i[2]) for i in l ]
    print l
    for y in range( 0, self.height-1):
      output = [] 
      for x in range( 5+offset, self.stride-1):
        if x > 115+offset:
          continue
        i = self.im[y][x]
        if (x,y) in l:
          output.append("B")
        elif i < 20:
          output.append(".")
        elif i < 64:
          output.append("+")
        elif i < 128:
          output.append("*")
        elif i < 196:
          output.append("x")
        else:
          output.append("X")
      print "%03d" % y, "".join(output)
    print "    56789 123456789 123456789 123456789 123456789 123456789 123456789 123456789 123456789 123456789"

  def applyFilter ( self, f, reshape=True ): 
    value = 0
    filt = getattr( self, f, False)
    if type(filt) == type(False):
      filt = numpy.array( getattr(filter, f, False), dtype=numpy.int )
      setattr( self, f, filt )
      if type(filt) == type(False):
        raise ValueError("Error: filter %s was not found in filter.py" % f)

    return convolve( self.im, filt, reshape )
      
  def findBarcode( self ):
    results = self.applyFilter("scaledFilter", reshape=False)
    list = [ (x[1], int(x[0] % self.stride), int(x[0] / self.stride)) for x in enumerate(results) if x[1] > 1000 ]
    list.sort(reverse=True)
    return list[0:20]

  def unAlias(s):
    "Remove dithering. "
    #s.im= ss.convolve2d( s.im, unAliasFilter, mode="same" )
    s.im=convolve( s.im, unAliasFilter, reshape=True )
    s.im=numpy.piecewise(s.im, [ s.im > 1000 ], [255, 0])
    return 
    """ Convolve operator does the following: 
    for y in range(1, s.height-1):
      for x in range(1, s.stride-1):
        if s.im[y][x-1] == s.im[y][x+1] == s.im[y+1][x] == s.im[y-1][x]: 
          s.im[y][x] = s.im[y][x+1]
    return
    """

  def bw( self, whitePoint=64):
    self.im=numpy.piecewise(self.im, [self.im < whitePoint, self.im >= whitePoint], [255, 0])
    #self.im=self.vApplyBW( self.im, whitePoint )
    
  def virtualLine(self, x1, y1, x2, y2, ox=0, oy=0):
    totalLength = math.sqrt(math.pow(x2-x1,2) + math.pow(y2-y1,2))
    if totalLength < 300:
      return []

    if x1 < x2:
      sx,sy,ex,ey=(x1,y1,x2,y2)
    else:
      sx,sy,ex,ey=(x2,y2,x1,y1)

    xgain = float(ex-sx)/totalLength
    ygain = float(ey-sy)/totalLength

    if ex - sx < 150:
      # Skip vertical codes, save them for the next run.
      return []
    if sx < 1 or (ex+ox) >= self.stride or sx > self.stride:
      return []
    if not (1< sy <self.height) or not (1< sy+ygain*totalLength <self.height):
      return []

    #slope = float(h2-h1)/(w2-w1) 
    newLine = numpy.zeros( shape=(totalLength), dtype=int )
    code = """
      float x=sx, y=sy;
      for ( int i=1; i < int(totalLength); i++ ) { 
        int  top = stride*int(y)    + int(x),
             bot = stride*int(y+1)  + int(x);
        float xr = x-int(x),
              xl = 1-xr,
              yt = y-int(y),
              yb = 1-yt;
        newLine[i]= im[top]*xr*yt   +
                    im[top-1]*xl*yt + 
                    im[bot]*xr*yb   +
                    im[bot-1]*xl*yb;
        x+=xgain;
        y+=ygain;
      }
    """

    stride, im = self.stride, self.im
    scipy.weave.inline(code,['im', 'stride', \
      'newLine', 'totalLength', 'ygain', 'xgain', 'sx', 'sy'])

    if DEBUG:
      log.debug( "".join( 
        [ chr( 0x2e + int(x/6.07142857142857142857) ) for x in list(newLine) ] ) ) 
    
    return newLine

  def checkLineCharacteristics( self, line ):
    whiteCount= blackCount= 0
    if 300 < len(line) < 475:
      for i in line:
        if int(i) < 128:
          whiteCount+=1
        else:
          blackCount+=1
        if whiteCount >= 18:
          return False
        if blackCount > 1:
          whiteCount=0
          blackCount=0
    else: 
      return False
    return True

  def getValidPoint ( self, point, possible ):
    for endpoint in possible:
      #print point, endpoint
      found = True
      for i in range ( 8, 50, 10 ):
        if not found:
          continue
        #print point, endpoint, i
        line = self.virtualLine(point[0]+2, point[1]+i, endpoint[0], endpoint[1]+i)
        if not self.checkLineCharacteristics(line):
          found = False
          #print "False"
        #print "True"
      if found: 
        return endpoint
    return False

    

  def getValidPair ( self, l, r ):
    """Returns the first pair that is a barcode and is located at the top
       edges of a barcode. """
    if not l or not r:
      return False
    l.sort( key=lambda x: x[1] ) 
    r.sort( key=lambda x: x[1] ) 

    if l[0][1] > r[0][1]:
      r.sort( key=lambda x: x[0], reverse=True )
      res = self.getValidPoint( l[0], r )
      if not res:
        return self.getValidPair( l[1:], r)
      return l[0], res
    else:
      l.sort( key=lambda x: x[0], reverse=False )
      res = self.getValidPoint( r[0], l )
      if not res:
        return self.getValidPair( l, r[1:] )
      return res, r[0]


  def removeNeighbors ( self, l, rev ):
    l.sort( key= lambda x: x[0], reverse=rev )
    restart = False
    sizeOfArray = len(l)-1
    for i in range (1, sizeOfArray):
      for j in range(i, sizeOfArray):
        if abs( l[i-1][1] - l[j][1] ) < 5:
          restart = True
          l[j] = False
      if restart==True:
        return self.removeNeighbors ([ x for x in l if x], rev)
    return l

  def getCode ( self, barcode ):
    """
    Return a single code from a code 128 barcode.
    """
    code=[]
    start = False
    trend = 1
    for pos, c in enumerate(barcode):
      if (pos+1) >= len(barcode):
        continue
      if not start:
        if c > int(10*250):  # Ignore leading white space
          start=True
          level = barcode[pos+1]
          code.append(pos)
        continue
      if abs(level - c) > 1250 and abs(level-barcode[pos+1]) > 1250:
        if (trend<0 and (level-c)>0) or (trend>0 and (level-c)<0):
          # Trend is in the same direction we are going, ignore.
          continue  
        code.append(pos) 
        if trend > 0:
          trend=-1
        else:
          trend=1
        level = c
      if trend > 0:
        level = max(c, level)
      else:
        level = min(c, level)
      if len(code) >= 7:
        return code, barcode[pos:]
    return False
      
  def applyHeuristics  ( self, barcode=[5,] ):
    """
    Try to determine the numerical values of barcode image.
    @barcode: list to prepend to output. (defaults to [5,])
    @return:  barcode weights (i.e. 211214...  prepended with pre)
    """

    rotated = numpy.rot90(self.im, 3)
    values = [ int(sum( list(line)[:30] )) for line in rotated ]
    characters=[]

    codes=True
    while (codes):
      codes = self.getCode(values)
      if codes:
        if DEBUG:
          print codes[0][0], codes[0][-1]
          print "".join([ "%c" % int(v/255+0x5f) for v in values[codes[0][0]:codes[0][-1]] ])
          print codes[0]
        characters.append(values[codes[0][0]:codes[0][-1]])
        values=codes[1]  
    return False


  def findBarcodeLimits( self, barType ):
    #origImg = self.im
    """ 
    find the edges of a barcode.
    @return: left and upper-right corner or right & upper-left corner of barcode
    """
    filterName = "%sEdgeFilter%s" % ("left", "Hard")
    result = self.applyFilter(filterName, reshape=False)

    leftSide, rightSide = [], []
    lSideLim, rSideLim = (self.stride / 2), ((self.stride/2)+1) 
    h,w=self.height,self.stride
    filterCutoff = 18000
    lx =  numpy.zeros( len(result), numpy.int )
    ly =  numpy.zeros( len(result), numpy.int )
    ry =  numpy.zeros( len(result), numpy.int )
    rx =  numpy.zeros( len(result), numpy.int )
    rets = numpy.zeros ( 2, numpy.int )
    l,r = 0,0
    filterlen= len(result)

    code = """
    int l=0, r=0;  /* This code is surprisingly slow in python */
    for (int i=0; i < filterlen; i++) {
      if (result[i] < filterCutoff)
        continue;
      if (i%w < lSideLim) {
        ly[l]   = i/w;
        lx[l++] = i%w;
      }
      if (i%w > rSideLim) {
        ry[r]   = i/w;
        rx[r++] = i%w;
      }
      rets[0] = l;
      rets[1] = r;
    }
    """

    scipy.weave.inline(code,['lx','rx','ry','ly','filterCutoff','filterlen','result', 'w', 'rSideLim', 'lSideLim','rets'])

    rx = rx[:rets[1]]
    lx = lx[:rets[0]]

    leftSide = zip(lx, ly)
    rightSide= zip(rx, ry)

    # We need to check the lists we generated to make sure we really have 
    # the furthest block for a specific height range...  We don't want to
    # be affected by artifacting which results in minor height variation.

    leftSide.sort (key = lambda x: x[0] )
    rightSide.sort(key = lambda x: x[0] )

    leftSide  = self.removeNeighbors( leftSide, False ) 
    

    #print "LEFT:  ", leftSide
    #print "RIGHT: ", rightSide

    validPair = self.getValidPair ( leftSide, rightSide )
    if not validPair:
      return False

    return ( (validPair[0][0]+2,validPair[0][1]+2), (validPair[1][0]+8, validPair[1][1]+2) )

hh=0
def straightenBarcode( im, filterName="Soft", prefix="" ):
  global hh, newImage
  hh+=1
  # Find the barcode, and straighten it. 
  im.bw()
  im.unAlias() 
  limits = im.findBarcodeLimits(filterName)
  if limits:
    if DEBUG:
      newImage.putdata(im.im.reshape(im.stride*im.height))
      newImage = ImageOps.invert(newImage)
      d = draw.Draw(newImage)
      d.line((limits[0][0], limits[0][1], limits[1][0], limits[1][1]), fill=0)
      newImage.save("%s.barcode.line.%05d.png" % (prefix, hh) )
    angle= ( float(limits[1][1] - limits[0][1]) / 
           float(limits[1][0] - limits[0][0])   )
    angle= numpy.arctan(angle) * (180/math.pi)
  else:
    return False
  im.im = scipy.ndimage.interpolation.rotate( im.im, angle, reshape=False )
  return True

def createBarcode( ar, nb ):
  ar=numpy.rot90(ar, 3)
  b,pos=1,0
  lastColor=False
  if not nb:
    return
  for bars in nb:
    if b % 2: 
      fill=255
    else:
      fill=0
    b+=1

    if pos > len(ar)-16:
      continue

    for i in range(0, bars*3):
      ar[pos].fill(fill)
      pos+=1


  for i in range(pos, len(ar)):
    ar[pos].fill(255)
    pos+=1
  return numpy.rot90(ar)

def doPostBarcodeAnalysis(image, prefix):
  image.save("%s.barcode.post.png" % prefix )
  bar = barImage( image )
  bar.bw()
  nb = bar.applyHeuristics()

  bar.im = createBarcode( bar.im, nb )

  image.putdata(bar.im.reshape(bar.stride*bar.height))
  #image = image.crop((1,2,450,88))
  image.save("%s.barcode.heur.png" % prefix )

newImage = False
def startRecognition( infile, rotation=False, z=0 ):
  global newImage
  prefix = infile[:8]
  im = Image.open(infile)
  if rotation:
    im = im.rotate(rotation)
  width, height = im.size
  resized = im.resize( ( width/25, height/30 ), Image.BICUBIC )
  resized = ImageOps.invert(resized)
  imgData = barImage( resized )
  foundBarcode, newImage, newBar = False, False, False

  for probable_barcode in imgData.findBarcode():
    z+=1
    # Try the first 20 barcodes, and see if one of them is legit.
    if foundBarcode:
      continue
    try: 
      x1, y1 = (probable_barcode[1]-3)*25, (probable_barcode[2]) * 30
      x2, y2 = x1+635, y1+265
      if x2 > im.size[0] or y2 > im.size[1]:
        x2,y2 = im.size[0], im.size[1]
        x1,y1 = im.size[0]-800, im.size[1]-265
      newImage = im.crop((x1,y1,x2,y2))
      newBar   = barImage(newImage)
      foundBarcode = straightenBarcode ( newBar, "Hard", prefix=prefix ) 
      if DEBUG and not foundBarcode:
        smoo = im.crop( (x1,y1,x2,y2) )
        smoo.save("%s.fail.%03d.barcode.png" % (prefix, z) )
        print "Z:  ", z
    except:
      foundBarcode = False
      raise

  if foundBarcode:
    log.info("Found barcode for %s." % prefix )
    newImage.putdata(newBar.im.reshape(newBar.stride*newBar.height))
    newImage = ImageOps.invert(newImage)
    newImage.save("%s.barcode.pre.png" % prefix )
    try: 
      (x1, y1),(x2,y2)  = newBar.findBarcodeLimits("Hard")
      doPostBarcodeAnalysis(newImage.crop((x1-40,y1+1,x1+520,y1+90)), prefix )
    except:
      pass
  elif not rotation:
    startRecognition( infile, rotation=90, z=z )
  else:
    log.info("No barcode found for %s.", prefix)

validImage = re.compile('[0-9]{4}-[0-9]{3}.png')
didCommandLine = False
for infile in sys.argv:
  if validImage.match(infile):
    didCommandLine = True
    startRecognition( infile )

if not didCommandLine:
  for infile in glob("????-???.png"):
    startRecognition( infile )


