# -*- coding: utf-8 -*-
# moo.
# (c) Charles Shiflett 2011

import sys

from mako.template import Template

import apps.forms.form_models.bform	 as bform
import apps.forms.form_models.bfbdb  as bfbdb
import apps.forms.form_models.bfsql  as bfsql
import apps.forms.form_models.templateLoader as templateLoader

import codecs

import pdb
import sys

def debugger(type, value, tb):
	"""
	Catch template errors with the debugger.
	"""
	pdb.pm()

sys.excepthook = debugger

# This file creates a tex document

def create_barcode( code ):
	barcode= { "code" : [] }
	shift=0
	rows=0
	h=5.0
	w=2.0

	for i in range(0,4):
		for j in range(0,16):
			shift=shift+1
			if code & 1:
				string = "\\draw (%2.5f,%2.5f) -- (%2.5f,%2.5f);" %(w/3,h/6,(w+0.5)/3,(h+1)/6)
			else:
				string = "\\draw (%2.5f,%2.5f) -- (%2.5f,%2.5f);" %((w+0.5)/3,h/6,w/3,(h+1)/6)
			barcode["code"].append( string )
			code=code/2
			w=w+0.5
		rows=rows+1
		shift=0
		h=h-1
		w=2.0

	return barcode

def texTrans( text ):
	return text.replace( "#", "\\#" )
	
def createTex ( formId, prefillData=None ):
	tagNames = "baseFont" # CSV we want to copy over to template.
	tex_file = []


	if prefillData:
		print "Prefill Not Implemented"

	form = bfbdb.loadObject( formId )
	formInfo = { 'formId': formId }
	ldr = templateLoader.templateLookup( themes=form.theme, output="tex"  )

	for tag in tagNames.split(","):
		if hasattr ( form, tag ) : 
			formInfo[tag] = getattr(form,tag)

	tex_file.append( ldr.render_to_string('header', formInfo )  )
	j=1



	for q in form.Questions:
		cntxt ={"q": q, "itemNumber": j }  
		tex_file.append( 
		  ldr.render_to_string( q.questionType, cntxt ).replace("\t","")   )
		if q.questionType < 256:
			j+=1

	tex_file.append( 
	  ldr.render_to_string('footer', create_barcode ( 0x12345678abcd0123 ))  )

	foutput = codecs.open ( "output.tex", "w", "utf-8" ) 

	for lines in tex_file:
		foutput.write( lines )

	foutput.close()


createTex(int(sys.argv[-1]))

