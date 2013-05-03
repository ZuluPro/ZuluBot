from django.conf.urls.defaults import *

urlpatterns = patterns('',
    url(r'^$', 'core.views.index', name='index'),
    url(r'^search_page$', 'core.views.search_page', name='search page'),
    url(r'^move_page$', 'core.views.move_page', name='move page'),
    url(r'^move_pages$', 'core.views.move_pages', name='move pages'),
    url(r'^add_category$', 'core.views.add_category', name='add category'),
    url(r'^move_category$', 'core.views.move_category', name='move category'),
    url(r'^add_category$', 'core.views.add_category', name='add category'),
    url(r'^remove_category$', 'core.views.remove_category', name='remove category'),
    url(r'^add_internal_link$', 'core.views.add_internal_link', name='add internal link'),
    url(r'^sub$', 'core.views.sub', name='sub'),

    url(r'^check_page$', 'core.views.check_page', name='check page'),
    url(r'^get_finished_tasks$', 'core.views.get_finished_tasks', name='Finished tasks'),
)
