from django.conf.urls.defaults import *

urlpatterns = patterns('',
    url(r'^$', 'core.views.index', name='index'),

    url(r'^add_user$', 'core.views.add_user', name='add user'),
    url(r'^update_user$', 'core.views.update_user', name='update user'),
    url(r'^delete_user$', 'core.views.delete_user', name='delete user'),
    url(r'^get_user$', 'core.views.get_user', name='get user'),
    url(r'^get_user_list$', 'core.views.get_user_list', name='get user list'),
    url(r'^set_active_user$', 'core.views.set_active_user', name='set active user'),

    url(r'^search_page$', 'core.views.search_page', name='search page'),
    url(r'^move_page$', 'core.views.move_page', name='move page'),
    url(r'^move_pages$', 'core.views.move_pages', name='move pages'),
    url(r'^add_category$', 'core.views.add_category', name='add category'),
    url(r'^move_category$', 'core.views.move_category', name='move category'),
    url(r'^add_category$', 'core.views.add_category', name='add category'),
    url(r'^remove_category$', 'core.views.remove_category', name='remove category'),
    url(r'^delete_category$', 'core.views.delete_category', name='delete category'),
    url(r'^add_internal_link$', 'core.views.add_internal_link', name='add internal link'),
    url(r'^sub$', 'core.views.sub', name='sub'),

    url(r'^get_page_text$', 'core.views.get_page_text', name='get page text'),
    url(r'^put_page_text$', 'core.views.put_page_text', name='put page text'),

    url(r'^search_contrib$', 'core.views.search_contrib', name='search contribution'),

    url(r'^check_page$', 'core.views.check_page', name='check page'),
    url(r'^get_page_links$', 'core.views.get_page_links', name='get page links'),
    url(r'^get_finished_tasks$', 'core.views.get_finished_tasks', name='Finished tasks'),
)
