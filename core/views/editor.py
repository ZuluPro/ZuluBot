from django.http import Http404, HttpResponse
from django.shortcuts import render, redirect
from django.contrib import messages
from django.conf import settings

from core.utils import method_restricted_to, is_ajax
from core.handlers import wiki_handler

@is_ajax()
@method_restricted_to('GET')
def get_page_text(request):
    w = wiki_handler()
    page = w.get_page(request.GET['q'])
    if page.exists():
        page_text = page.get()
    else:
        page_text = ''
    return HttpResponse(page_text)

@is_ajax()
@method_restricted_to('POST')
def put_page_text(request):
    w = wiki_handler()
    page = w.get_page(request.POST['page'])
    page.put(request.POST['text'], request.POST['comment'])
    messages.add_message(request, messages.SUCCESS, u"Publication effectu\xe9e.")
    return render(request, 'base/messages.html', {
        'messages':messages.get_messages(request),
    })
