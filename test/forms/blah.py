# -*- coding: utf-8 -*-
from django.core.management import setup_environ


import forms.form_models.bfsql as bfsql
import forms.form_models.bform as bforms
from forms.form_models.bfbdb import *

bf = bforms.BerkeleyForm()
bf.theme=('columns',)

"""
Don't just write documents, create an information workflow. Berkeley Forms
is the solution to collecting, managing, storing, and analyzing data.

Berkeley forms makes IT easy!
"""

qdb = [
	{'type':'Section','label':'Your Contact Information\n \ \n\n ','style':'section'},
	{'type':'Info','label':'An Info Boxxer\n\n\n '},
	{'type':'Text','label':'Name: ','style':{'grid': (1,4,8)}},
	{'type':'Text','label':'Date:', 'style': {'grid':(1,2,8)}},
	{'type':'Text','label':'Phone:', 'style': {'grid':(1,3,8)} },
	{'type':'Text','label':'Email:','style': {'grid':(1,3,8),}},

	{'type':'Section','label':'Features needed from Berkeley Forms','style':'section'},

		{'type':'CheckMany',
			'label':'Languages:',
			'style': {'grid': (16, 3, 1, 16)},
		'choices':(
		'English',
		{'label': 'العربية', 'direction': 'rtl'},
		u'Català',
		u'Česky',
		u'Dansk',
		u'Deutsch',
		u'Español',
		u'Français',
		{'label': u'فارسی', 'direction': 'rtl'},
		{'label': u'עברית', 'direction': 'rtl'},
		'Italiano',
		u'한국어',
		'Magyar',
		u'日本語',
		u'Norsk (bokmål)',
		u'Polski',
		u'Русский',
		u'Română',
		u'Slovenčina',
		u'Suomi',
		u'Svenska',
		u'ภาษาไทย',
		u'Türkçe',
		u'Українська',
		u'Volapük',
		u'中文'
		)},
		{'type':'Text','label':'Please list any other MEDICAL CONDITIONS not mentioned above:'},

	{'type':'Text','label':'Completed On: '},
	]

bforms.createQuestions(bf,qdb)
print saveObject(bf)

