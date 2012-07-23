# -*- coding: utf8 -*-
from django.template import Context, loader
from django.shortcuts import render_to_response
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse

from pages.models import details, addCat
import sys, re ; sys.path.append('/Library/Frameworks/Python.framework/Versions/2.7/lib/python2.7/site-packages/pywikipedia/')
import wikipedia

def oeuvre(request, pagename) :
	page = details(pagename, 'article')
	if not page : page = { 'error':"Pas d'infobox sur l'article" }
	return HttpResponse( loader.get_template( 'page.html').render(Context( dict( page.items()+[('oeuvrepage',True)] ) )) )

def preview(request, pagename, field=None) :
	print request.POST
	if request.method == "POST"  :
		if "cancel_q" in request.POST.keys() : return HttpResponseRedirect('/category/'+catname)
		addCat( pagename, request.POST.values() , 'article', misc='label')
		return HttpResponseRedirect('/article/'+pagename+'/oeuvre')
	else :
		page = details(pagename, 'article')
		pagetext = page['Page'].get()
		modificationList = []
		for unit in page['contentsDict']['label'] :
			if re.search( r"\[\[Cat.gorie:Album publi. par "+unit[0] , pagetext ) : modificationList.append( ( unit[0], False ) )
			else : modificationList.append( ( unit[0], True ) )
		return HttpResponse( loader.get_template( 'page.html').render(Context( { 'type':'article', 'modificationList':modificationList, 'title':pagename } )) )

def categoryPreview(request, catname ) :
	if request.method == 'POST' :
		if "cancel_q" in request.POST.keys() : return HttpResponseRedirect('/category/'+catname)
		toAddDict = {}
		for modif in request.POST.keys() :
			m = re.search(r"///" , modif )
			pagename, category = modif[:m.start()].replace('_',' ') , modif[m.end():].replace('_',' ')
			if not pagename in toAddDict.keys() :
				toAddDict[pagename] = []
				toAddDict[pagename].append( category )
			else : toAddDict[pagename].append( category )
		for pagename,categories in toAddDict.items() :
			addCat( pagename, categories, 'article', misc='label')
		return HttpResponseRedirect('/category/'+catname)

	## Affichage du formulaire
	category = details(catname, 'category')
	modificationDict = {} 
	for article in category['articlesList'] :
		print article.title()
		article = details(article.title(), 'article' )
		modificationDict[article['title']] = []
		pagetext = article['Page'].get()
		if 'label' in article['contentsDict'].keys() :
			error = []
			for unit in article['contentsDict']['label'] :
				try :
					if re.search( r"\[\[Cat.gorie:Album publi. par "+ re.sub(r"(\(|\))", r".", unit[0]) , pagetext ) :
						modificationDict[article['title']].append( ( unit[0], False  ) )
					else : modificationDict[article['title']].append( ( unit[0], True ) )
				except : error.append( unit )
	return HttpResponse( loader.get_template( 'boxtocat.category.preview.html').render(Context( { 'type':'category', 'modificationDict':modificationDict, 'title':catname, 'cats':category['articlesList'] } )) )
