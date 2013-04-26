from django import template
register = template.Library()

from core.handlers import wiki_handler

@register.filter(name='get_full_url', is_safe=True)
def get_full_url(page, link=None):
    w = wiki_handler()
	full_url = w.dbuser.url+page.urlname()
	if not link:
        return full_url
	else:
        html = '<a href="%s"><i class="icon-search"></i></a>' % full_url
        return html
