from django.shortcuts import render, redirect
from django.contrib import messages
from django.conf import settings

from djcelery.models import TaskMeta

from core.tasks import async_move_pages, async_add_category, async_move_category
from core.utils import make_messages
from core.handlers import wiki_handler
w = wiki_handler()

def index(request):
    return render(request, 'index.html', {
        'title':'ZuluBot',
    })

def search_page(request):
    if request.GET.get('type','content') == 'content':
        results = [ p for p in w.search_words(request.GET['q']) ]
    else:
        results = [ p for p in \
            w.search_in_title(request.GET['q'], namespaces=request.GET.get('type',None)) ]
    
    return render(request, 'option.html', {
        'pages':results,
    })

def move_page(request):
    w.move_page(request.POST['from'], request.POST['to'])
    messages.add_message(request, messages.INFO, 'Action en cours.',
                                 fail_silently=True)
    return render(request, 'base/messages.html', {
        'messages':messages.get_messages(request),
    })

def move_pages(request):
    pages = request.POST.getlist('pages[]')
    if len(pages) > 0 and 'djcelery' in settings.INSTALLED_APPS :
        async_move_pages.delay(pages, request.POST['from'], request.POST['to'], request.POST['redirect'])
        messages.add_message(request, messages.INFO, 'Renommage en cours.')
        msgs = messages.get_messages(request)
    else:
        results = w.move_pages(pages, request.POST['from'], request.POST['to'], request.POST['redirect'])
        msgs = make_messages(request, results)

    return render(request, 'base/messages.html', {
        'messages':msgs,
    })

def check_page(request):
    p = w.get_page(request.GET['page'])
    if p.exists():
        messages.add_message(request, messages.SUCCESS, 'Correcte.',
                                     fail_silently=True)
    else:
        messages.add_message(request, messages.WARNING, 'Introuvable.',
                                     fail_silently=True)
    return render(request, 'base/messages.html', {
        'messages':messages.get_messages(request),
    })
    
def add_category(request):
    pages = request.POST.getlist('pages[]')
    if len(pages) > 3 and 'djcelery' in settings.INSTALLED_APPS :
        async_add_category.delay(pages, request.POST['category'])
        messages.add_message(request, messages.INFO, u'Ajout de cat\xe9gorie en cours.')
        msgs = messages.get_messages(request)
    else:
        results = w.add_category(pages, request.POST['category'])
        msgs = make_messages(request, results)

    return render(request, 'base/messages.html', {
        'messages':msgs,
    })

def move_category(request):
    if 'djcelery' in settings.INSTALLED_APPS :
        async_move_category.delay(request.POST['from'], request.POST['to'])
        messages.add_message(request, messages.INFO, u'D\xe9placement de cat\xe9gorie en cours.')
    else:
        w.move_category(request.POST['from'], request.POST['to'])
        messages.add_message(request, messages.INFO, u'D\xe9placement de cat\xe9gorie termin\xe9.'),
    return render(request, 'base/messages.html', {
        'messages':messages.get_messages(request),
    })

def remove_catgory(request):
    pages = request.POST.getlist('pages[]')
    if 'djcelery' in settings.INSTALLED_APPS :
        async_remove_category_from.delay(pages, request.POST['category'])
        messages.add_message(request, messages.INFO, u'Suppression de cat\xe9gorie en cours.')
        msgs = messages.get_messages(request)
    else:
        w.remove_category_from(pages, request.POST['category'])
        messages.add_message(request, messages.INFO, u'D\xe9placement de cat\xe9gorie termin\xe9.'),
        msgs = make_messages(request, results)

    return render(request, 'base/messages.html', {
        'messages':messages.get_messages(request),
    })


def get_finished_tasks(request):
    results = [ t.result  for t in TaskMeta.objects.all() ]
    [ t.delete()  for t in TaskMeta.objects.filter(status='SUCCESS') ]
    return render(request, 'base/messages.html', {
        'messages':make_messages(request, results),
    })
    
