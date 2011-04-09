"""
  " (c) Charles Shiflett 2011
  "
  "" "" "" "" "" "" "" "" "" "" "" "" """

from django.http             import HttpResponse
from django.conf             import settings
from pyPdf import PdfFileWriter, PdfFileReader

documentRoot = settings.SCAN_UPLOADS
pdfCache = settings.PDFCACHE

def createPDF(pdfKey, pageStart, count):

  output = PdfFileWriter()
  
  project = PdfFileReader(file(str("%s/%s/%s.pdf" % ( documentRoot, pdfKey, pdfKey )), "rb") )
  end = int(pageStart) + int(count) 

  if end > project.getNumPages():
    end = project.getNumPages() +1


  for i in range(int(pageStart), int(end)):
    output.addPage(project.getPage(i-1))

  outFile = file(str("%s/%s-%s-%s.pdf" % 
    ( pdfCache, pdfKey, pageStart, count ) ) , "wb" )

  output.write(outFile)


def gen( request, pdfKey, pageStart, count ):
  try: 
    z=open("%s/%s-%s-%s.pdf" % (pdfCache, pdfKey, pageStart, count), "r")
  except:
    createPDF(pdfKey, pageStart, count)
    z=open("%s/%s-%s-%s.pdf" % (pdfCache, pdfKey, pageStart, count), "r")

  return HttpResponse ( z.read(), mimetype="application/pdf" )

