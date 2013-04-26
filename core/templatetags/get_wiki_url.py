from django import template
register = template.Library()

from core.handlers import wiki_handler

@register.filter(name='get_wiki_url', is_safe=True)
def get_wiki_url(page, link=None):
    w = wiki_handler()
	return w..get_wiki_url(page,True)
