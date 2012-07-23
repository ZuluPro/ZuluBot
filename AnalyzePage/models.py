from django.db import models
from django import forms
import sys, re
sys.path.append('/Library/Frameworks/Python.framework/Versions/2.7/lib/python2.7/site-packages/pywikipedia/')
import wikipedia, infoboxMusique

language = "fr"
family = "wikipedia"
mynick = "-Nmdbot"
site = wikipedia.getSite(language,family)

class Page(forms.Form):
    pagename = forms.CharField(max_length=200)

def pagedetails(pagename):
	page = dict()
	page['Page'] =  wikipedia.Page(site, pagename )
	try : page['text'] = page['Page'].get()
	except IsRedirectPage :
		page['Page'] = wikipedia.Page(site, re.sub(r".*'(.*)'.*", r"\1", str(sys.exc_info()[1]) ) )
		page['text'] = page['Page'].get()
	page['title'] = page['Page'].title()
	page['infobox'] = infoboxMusique.InfoboxMusiqueAlbum(page['Page'])
	page['categories'] = page['Page'].categories(api=False)
	return dict( page.items() + page['infobox'].contents.items() )

def pagedetailsTest() :
	page = dict()
	page['Page'] = wikipedia.Page(site, 'Test' )
	page['text'] = 'Contenu de la page de test'
	page['title'] = 'Test'
	return page	
