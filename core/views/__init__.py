from django.conf import settings

if 'djcelery' in settings.INSTALLED_APPS:
	CELERY_IS_ACTIVE = True
	from djcelery.models import TaskMeta
	from core.tasks import async_move_pages, async_add_category, async_move_category, \
			async_remove_category, async_add_internal_link, async_sub
else:
	CELERY_IS_ACTIVE = False

from views import index, search_contrib
from actions import search_page, move_page, move_pages, check_page, add_category, \
        move_category, remove_category, add_internal_link, sub, get_finished_tasks, \
        get_page_links
from editor import get_page_text, put_page_text
from user import add_user, get_user, update_user, get_user_list, delete_user, set_active_user
