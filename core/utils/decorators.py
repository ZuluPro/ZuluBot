from django.http import Http404
from django.conf import settings

class method_restricted_to(object):
    """
    Restrict view to the given list of method.
    Raise 404 if method isn't allowed.
    """
    def __init__(self, methods=[]):
        self.methods = methods

    def __call__(self, f):
        def wrapped_f(request, *args):
            if request.method in self.methods:
                return f(request, *args)
            else:
                raise Http404
            
        return wrapped_f

class is_ajax(object):
    """
    Restrict view to ajax client.
    Raise 404 if DEBUG = True
    """
    def __call__(self, f):
        def wrapped_f(request, *args):
            if not request.is_ajax() and not settings.DEBUG:
                raise Http404
            else:
                return f(request, *args)
            
        return wrapped_f
