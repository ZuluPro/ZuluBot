from django.conf.urls import patterns, include, url
from django.conf import settings
from pages import views
# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
    url(r'^static/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.STATIC_ROOT }),
    url(r'^pywiki/category$', 'pywikipedia.views.category'),
    url(r'^Zulubot$', 'pages.views.zulubot'),
    url(r'^category/(?P<catname>.*)/preview$', 'boxToCat.views.categoryPreview'),
    url(r'^article/(?P<pagename>.*)/oeuvre$', 'boxToCat.views.oeuvre'),
    url(r'^article/(?P<pagename>.*)/oeuvre/preview$', 'boxToCat.views.preview'),
    url(r'^results/(?P<type>(article|page|category|user|template))$', 'pages.views.results'),
    url(r'^(?P<type>(article|page|category|template|user))/(?P<pagename>[^/]*)/(?P<discussion>discussion)/edit$', 'pages.views.edit'),
    url(r'^(?P<type>(article|page|category|template|user))/(?P<pagename>[^/]*)/edit$', 'pages.views.edit'),
    url(r'^(?P<type>(article|page|category|template|user))/$', 'pages.views.articleIndex'),
    url(r'^(?P<type>(article|page|category|template|user))/(?P<pagename>.*)/discussion$', 'pages.views.discussion'),
    url(r'^(?P<type>(article|page|category|template|user))/(?P<pagename>.*)/?$', 'pages.views.article'),
    #url(r'^page/$', 'pages.views.pageIndex'),
    url(r'^$', 'pages.views.index'),
)
