from django.db import models
import sys, re
sys.path.append('/Library/Frameworks/Python.framework/Versions/2.7/lib/python2.7/site-packages/pywikipedia/')
import wikipedia, catlib, infoboxMusique

language = "fr"
family = "wikipedia"
mynick = "-Nmdbot"
site = wikipedia.getSite(language,family)

pageColors = { 'article':'rgb(255, 128, 128)', 'page':'rgb(255, 128, 128)', 'category':'rgb(128, 255, 128)', 'discussion':'rgb(218,165,32)', 'user':'rgb(218,165,32)', 'template':'rgb(107,142,35)',
	'discussion':'rgb(205,133,63 )',
	'album':'rgb(135, 206, 250)', 'live':'rgb(255,204,153)', 'EP':'rgb(255,186,159)', 'compilation':'rgb(233,198,176)', 'remix':'rgb(255,218,185)', u'vid\xe9o':'rgb(248,248,255)',
	'bande originale':'rgb(153,204,204)', 'single':'rgb(244,220,182)', 'chanson':'rgb(223,228,251)',
}

NamespaceDict = { }
for key in pageColors :
	NamespaceDict[key] = 0
NamespaceDict['articlediscussion'] = 1
NamespaceDict['discussion'] = 1
NamespaceDict['user'] = 2
NamespaceDict['userdiscussion'] = 3
NamespaceDict['template'] = 10
NamespaceDict['templatediscussion'] = 11
NamespaceDict['category'] = 14
NamespaceDict['categorydiscussion'] = 15

def testInternet() :
	try : f = urllib2.urlopen('http://www.python.org/') ; return True
	except : return False

def addCat(pagename, catList, pType, misc='' ) :
	if misc=='label' : misc=u'Album publi\xe9 par '
	page = wikipedia.Page(site, pagename, defaultNamespace=NamespaceDict[pType] )
	if page.isRedirectPage() == True : page = page.getRedirectTarget()

	pagetext = page.get() 

	if type(catList) == type('') : catList = [ catList ]
	comment = u'+Cat\xe9gorie '
	newtext = pagetext
	for cat in catList :
		if not re.search( r"\[\[Cat.gorie:"+misc+cat, newtext ) :
			comment += ' '+cat+' '
			newtext = re.sub( r"(\[\[Cat.gorie:.*\n)", r"\1"+u"[[Cat\xe9gorie:"+misc+cat+"]]\n", newtext, 1 )
	if pagetext != newtext :
		wikipedia.Page(site, pagename, defaultNamespace=NamespaceDict[pType] ).put( newtext=newtext, comment=comment )

def checkpage(pagename, type='page'):
	if wikipedia.Page(site, pagename, defaultNamespace=NamespaceDict[type] ).exists() == False : return ('404','Page '+pagename+' non existante')
	#if catlib.Category(site, pagename ).exists() == False : return ('404','Categorie '+pagename+' non existante')
	else : return ('OK', wikipedia.Page(site, pagename, defaultNamespace=NamespaceDict[type] ).titleWithoutNamespace() )

def details(pagename, type, api=False, discussion=''):
	page = dict()
	page['Page'] = wikipedia.Page(site, pagename, defaultNamespace=NamespaceDict[type+discussion] )
	if page['Page'].isRedirectPage() == True :
		page['redirectFrom'] = page['Page']
		page['Page'] = page['Page'].getRedirectTarget()
	if type == 'category' and not discussion :
		page['Page'] = catlib.Category(site, pagename ) 
		page['articlesList'] = page['Page'].articlesList()
		page['subcategoriesList'] = page['Page'].subcategoriesList()
		page['types'] = [ 'category' ]
		api=True
	elif type == 'template' and not discussion :
		page['fieldList'] = [ line.lower() for line in re.sub( r".*\{\{\{([^(\|?\}\}\})]*)\|?\}\}\}.*", r"\2", wikipedia.Page( site, pagename, defaultNamespace=10 ).get() , re.DOTALL ).split('\n') if re.match( r"\w", line ) ]
		[ page['fieldList'].pop(i) for i in range(len(page['fieldList']))[::-1] if page['fieldList'].count(page['fieldList'][i]) > 1 ]
		page['types'] = [ 'template' ]
	else : page['types'] = [ 'article' ]
	if discussion : page['discussion'] = 'discussion'

	tempList = [ temp[0] for temp in page['Page'].templatesWithParams() ]
	if ( u'Infobox Musique (oeuvre)' in tempList ) or ( u'Infobox Musique (\u0153uvre)' in tempList ) :
		box = infoboxMusique.InfoboxMusiqueAlbum(page['Page'])
		page['contents'] = box.contents
		page['contentsDict'] = box.contentsDict
		page['types'].append( box.contents['charte'] )
	else : page['contentsDict'] = {}
	page['title'] = page['Page'].titleWithoutNamespace()
	page['urlname'] = page['Page'].urlname()
	page['templates'] = page['Page'].templates()
	try : page['versionHistory'] = page['Page'].getVersionHistory() # Liste de liste : id,date,user,comment
	except : pass
	#page['latestEditors'] = page['Page'].getLatestEditors()
	page['linkedPages'] = page['Page'].linkedPages()
	[ page['linkedPages'].pop(i) for i in range(len(page['linkedPages']))[::-1] if page['linkedPages'].count(page['linkedPages'][i]) > 1 ]
	page['categories'] = page['Page'].categories(api=api)
	page['type'] = type
	page['color'] = pageColors[type]
	# Liste des utilisateurs
	page['latestEditors'] = page['Page'].getLatestEditors()
	return page

