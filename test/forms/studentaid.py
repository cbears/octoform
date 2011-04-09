# -*- coding: utf-8 -*-
from django.core.management import setup_environ


import forms.form_models.bfsql as bfsql
import forms.form_models.bform as bforms
from forms.form_models.bfbdb import *

bf = bforms.BerkeleyForm()
bf.baseFont='palatino'
bf.theme=('demos',)

"""
Don't just write documents, create an information workflow. Berkeley Forms
is the solution to collecting, managing, storing, and analyzing data.

Berkeley forms makes IT easy!
"""

qdb = [
	{'type': 'Info',
	 'label':'|bold||large||larger|THANK YOU|/larger| for visiting the Student Aid office. By answering the questions below, you can help us improve our services to students.\n \ \n\n |/large||/bold|',
	 'style': {'font': 'buffy'}},
	{'type': 'Section', 'key': 12345, 'style': {'start': True, 'layout': 'list', 'columns': 1}, 'label': ' '  }, 
	{'type': 'Info',
	 'label':'Your input is valued, regardless of how positive or negative your experience was today.',
	 'style': {'layout': 'list'}},
	{'type':'Info','label':'The questionnaire should take you less than 5 minutes.',
	 'style': {'layout': 'list'}},
	{'type':'Info','label':'Your responses will be kept confidential and will not be associated with your name, ever.',
	 'style': {'layout': 'list'}},
	{'type':'Info','label':'When you are finished, you may fold this form and place it in the box at the Student Aid desk, or drop it in campus mail if folded so the campus mail address is exposed.',
	 'style': {'layout': 'list'}},
	{'type': 'Section', 'key': 12345, 'style': {'end': True, 'layout': 'list'}, 'label': ' ' }, 
	{'type':'Info', 
			'label':'|invert||bold|Why did you visit the student aid office today?|/bold||br||indent||italic|Please Check all that apply |/italic||OCR||/invert|' },
	{'type': 'CheckMany',
			'style': {'layout': 'column', 'columns': 2},
		'choices':(
			'To resolve a problem',
			'To ask a question specific to my financial aid',
			'To ask a general question about student aid',
			'To get general information',
			'Other: |ul|'
	)},
	{'type':'Info','label':"""
		|invert||bold||small|
		For the statements below, strike the choice to the right that indicates how much you agree or disagree
		|/small||/bold||br||italic||indent|
		If the statement does not apply to your experience, choose ``NA.''
		|/italic||/invert|
	 """},


{'type': 'Section', 'key': 12346, 'style': {
	 'start': True, 
	 'layout': 'grid', 
	 'dimension': (10,4,1), 
	 'label': ' '  
	}
}, 

	{'type':  'Info',
	 'label': '',
	 'style': {'layout': 'grid', 'rotate': 315, 'shift': -.325}, 
	 'choices': (
	   '|small|Strongly Disagree|/small|', 
		 '|small|Disagree|/small|',
		 '|small|Neither Agree nor Disagree|/small|',
		 '|small|Agree|/small|',
		 '|small|Strongly Agree|/small|',
		 '|small|NA|/small|'
	 )},
	{'type' :  'CheckOne',
	 'label':  'I am satisfied with the outcome of my visit',
	 'style': {'layout': 'grid'}, 
	 'choices': ( 'SD', 'D', 'N', 'A', 'SA', 'NA') },

	{'type' :  'CheckOne',
	 'label':  'I felt welcome during my visit',
	 'style': {'layout': 'grid'}, 
	 'choices': ( 'SD', 'D', 'N', 'A', 'SA', 'NA') },

	{'type' :  'CheckOne',
	 'label':  'I was able to accomplish the task I visited for',
	 'style': {'layout': 'grid'}, 
	 'choices': ( 'SD', 'D', 'N', 'A', 'SA', 'NA') },

	{'type' :  'CheckOne',
	 'label':  'I understand any future steps I must take to resolve my problem/question',
	 'style': {'layout': 'grid'}, 
	 'choices': ( 'SD', 'D', 'N', 'A', 'SA', 'NA') },

	{'type' :  'CheckOne',
	 'label':  'I am confident that future visits to this office will be productive',
	 'style': {'layout': 'grid'}, 
	 'choices': ( 'SD', 'D', 'N', 'A', 'SA', 'NA') },

{'type': 'Section', 'key': 12346, 'style': {'end': True,  'columns': 1, 'layout': 'grid'}, 'label': ' '  }, 

{'type':'Info','label':"""
		|invert||bold| 
		The following questions help us understand why your experiences may differ from other students.
		|/bold||br||italic||indent|
		Please select an answer to the right.
		|/italic||/invert|
		""" },

{'type': 'Section', 'key': 12347, 'style': {
	'start': True, 
	'layout': 'grid', 
	'dimension': (10,4,1), 
	'label': ' '  } 
}, 

	{'type' :  'CheckOne',
	 'label':  'How many times have you visited the student aid office for |bold|this specific reason|/bold|?  ',
	 'style': {'layout': 'grid'}, 
	 'choices': ( '0', '1', '2', '3', '4', '5+') },

	{'type' :  'CheckOne',
	 'label':  'How many times have you visited the student aid office for |bold|other reasons|/bold| in the past?  ',
	 'style': {'layout': 'grid'}, 
	 'choices': ( '0', '1', '2', '3', '4', '5+') },

	{'type' :  'CheckOne',
	 'label':  'Were you referred to another office at Eastern University during your visit?  ',
	 'style': {'layout': 'grid'}, 
	 'choices': ( 'Yes', 'No' ) },



{'type': 'Section', 'key': 12347, 'style': {'end': True, 'layout': 'grid', 'dimension': (10,4,1), 'label': ' '  }}, 

	{'type':'Info','label':'Completed On: '},
	]

bforms.createQuestions(bf,qdb)
