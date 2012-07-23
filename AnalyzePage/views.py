# -*- coding: utf8 -*-
# 22/06/12 - Par Anthony MONTHE

from django.template import Context, loader
from django.http import HttpResponse
from django.db.models import Q
from AnalyzePage.models import *
import sys ; sys.path.append('/Library/Frameworks/Python.framework/Versions/2.7/lib/python2.7/site-packages/pywikipedia/')
import wikipedia, catlib

language = "fr"
family = "wikipedia"
mynick = "-Nmdbot"
site = wikipedia.getSite(language,family)


def index(request) :
	t = loader.get_template('index.html').render(Context({}))
	return HttpResponse(t)

def result(request) :
	if request.method == 'POST': 
		if isEmpty() :
			t = loader.get_template('results.err.html').render(Context({'error':'Categorie vide !'}))
			return HttpResponse(t)
		else :	
			catlist = catlib.Category(site, request._get_post()['catname'] ).articlesList()
			catlist = [ x.title() for x in catlist ] 
			t = loader.get_template('results.html').render(Context({ 'catlist':catlist}))
			return HttpResponse(t)
	else :	
		t = loader.get_template('results.err.html').render(Context({'error':'Pas de requête'}))
		return HttpResponse(t)

def page(request, pagename) :	
	t = loader.get_template('page.html').render(Context(
		pagedetails(pagename)
	))
	return HttpResponse(t)

def pageTest(request) :	
	t = loader.get_template('page.html').render(Context(
		pagedetailsTest()
	))
	return HttpResponse(t)
