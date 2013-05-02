from django import template
from urllib2 import unquote

register = template.Library()


@register.filter(name='unurlize')
def unurlize(string, arg=None):
    """Convert URL string to unicode."""
    if string and isinstance(string, basestring):
        return unquote(string).decode('utf8')
