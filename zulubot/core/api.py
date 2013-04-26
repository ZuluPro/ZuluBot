from django.views.decorators.csrf import csrf_exempt 
from django.http import HttpResponse
from django.utils.timezone import now

from SimpleXMLRPCServer import SimpleXMLRPCDispatcher
from datetime import datetime

dispatcher = SimpleXMLRPCDispatcher(allow_none=True, encoding=None)

@csrf_exempt 
def webservice(request):
    """
    the actual handler:
    if you setup your urls.py properly, all calls to the xml-rpc service
    should be routed through here.
    If post data is defined, it assumes it's XML-RPC and tries to process as such
    Empty post assumes you're viewing from a browser and tells you about the service.
    """

    if len(request.POST):
        response = HttpResponse(mimetype="application/xml")
        response.write(dispatcher._marshaled_dispatch(request.raw_post_data))
    else:
        response = HttpResponse()
        response.write("<b>This is an XML-RPC Service.</b><br>")

    response['Content-length'] = str(len(response.content))
    return response

def test():
    """A simple test for webservice."""
    return 0

def search(word):
    """A simple test for webservice."""
    return 0

dispatcher.register_function(test, 'test')
dispatcher.register_function(search, 'search')
