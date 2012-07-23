# -*- coding: utf8 -*-
# 22/06/12 - Par Anthony MONTHE

from django.template import Context, loader
from django.shortcuts import render_to_response
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse

from pages.models import *
from pages.forms import PageForm
import sys ; sys.path.append('/Library/Frameworks/Python.framework/Versions/2.7/lib/python2.7/site-packages/pywikipedia/')
import wikipedia, catlib

language = "fr"
family = "wikipedia"
mynick = "-Nmdbot"
site = wikipedia.getSite(language,family)

#####
def index(request):
	if request.GET != {} :
		pageGet = ''
		try :
			pageGet = request.GET['page_q']
		except : pass
		if pageGet != '' :
			if request.GET['page_q'] == 'test' :
				return HttpResponseRedirect(reverse('pages.views.pageTest'))
			return HttpResponseRedirect(reverse('pages.views.page', args=(request.GET['page_q'],)))
		return HttpResponseRedirect('/page/')
	else:
		print request.POST
		form = PageForm()
		return render_to_response('index.html', {'form': form})
#####

#def index(request) :
#	t = loader.get_template('index.html').render(Context({}))
#	return HttpResponse(t)

def zulubot(request) :	
	connection = testInternet()	
	return HttpResponse( loader.get_template( 'zulubot.html').render(Context( { 'connection':connection } )) )

def edit(request, pagename, type, discussion=None) :	
		if discussion == 'discussion' : return edit(request, pagename, type, '/discussion')
		elif discussion == None : discussion = ''
		if request.method == 'POST' :
			if 'pagetext_cancel_q' in request.POST : return HttpResponseRedirect('/'+type+'/'+pagename+discussion)
			elif 'pagetext_q' in request.POST :
				wikipedia.Page(site, pagename, defaultNamespace=NamespaceDict[type+discussion[1:]] ).put( request.POST['pagetext_q'], comment=request.POST['comment_q'] )
				return HttpResponseRedirect('/'+type+'/'+pagename+discussion)
		else :
			page = wikipedia.Page(site, pagename, defaultNamespace=NamespaceDict[type+discussion[1:]] )
			if not page.exists() :
				return HttpResponse( loader.get_template( 'page.edit.html').render(Context( { 
					'color' : pageColors[type], 'title' : page.title(), 'error':'Page non existante !', 'type':type } )) )
			return HttpResponse( loader.get_template( 'page.edit.html').render(Context( {
				'color' : pageColors[type],
				'pagetext' : page.get(),
				'title' : page.titleWithoutNamespace(),
				'type':type,
				'discussion':discussion,
			 } )) )

def discussion(request, pagename, type) :
	if checkpage(pagename, type+'discussion')[0] == '404' :
		return edit(request, pagename, type, 'discussion')
	else :
		return HttpResponse( loader.get_template( 'discussion.html').render(Context( details(pagename,type,discussion='discussion') )) ) 

def results(request, type) :	
	results = list( site.search( request.GET[type+'_q'], number=100, namespaces=NamespaceDict[type] ) )
	return HttpResponse( loader.get_template( 'results.html').render(Context( { 
		'title':request.GET[type+'_q'], 'color':pageColors[type], 'results':results, 'type':type,
	} )) ) 

def articleIndex(request, type) :	
	if len(request.GET) > 0 :
		pagename = request.GET[type+'_q']
		if pagename == '' : return HttpResponse( loader.get_template(type+'.index.html').render(Context( { 'color':pageColors[type], 'type':type } )) )
		return HttpResponseRedirect('/'+type+'/'+pagename)
	else :
		return HttpResponse( loader.get_template( type+'.index.html').render(Context( { 'color':pageColors[type], 'type':type } )) )

def article(request, type, pagename=None, discussion=None ) :	
	if discussion == 'discussion' : return article(request, type, pagename, '/discussion')
	elif discussion == None : discussion = ''
	if request.method == 'POST' :
		if 'category_add_q' in request.POST.keys() : addCat(pagename, request.POST['category_add_q'], 'category' )
		if 'page_add_q' in request.POST.keys() : addCat( pagename, request.POST['page_add_q'], 'page' )
		return HttpResponseRedirect('/'+type+'/'+pagename+discussion)
	if len(request.GET) > 0 :	## Si le GET pas vide
		if pagename == '' :		## Si la vue n'a pas de pagename
			pagename = request.GET[type+'_q']	
			if pagename == '' : return HttpResponseRedirect('/'+type+'/'+pagename+discussion) 
		else :
			return HttpResponseRedirect('/'+type+'/'+pagename+discussion)
	if checkpage(pagename, type)[0] != '404' :
		return HttpResponse( loader.get_template(type+'.html').render(Context( details(pagename, type, discussion=discussion) )) )
	else : return HttpResponse( loader.get_template('page.edit.html').render(Context( { 'color' : pageColors[type], 'title':pagename, 'error':checkpage(pagename, type)[1] } )) )

