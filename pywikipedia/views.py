from django.template import Context, loader
from django.shortcuts import render_to_response
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse

from pages.models import details, addCat
import sys, re ; sys.path.append('/Library/Frameworks/Python.framework/Versions/2.7/lib/python2.7/site-packages/pywikipedia/')
import wikipedia

def category(request)  :
	return HttpResponse( loader.get_template( 'pywiki.category.html').render(Context( {} )) )

