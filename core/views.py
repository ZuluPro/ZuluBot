from django.http import Http404
from django.shortcuts import render, redirect
from django.contrib import messages
from django.conf import settings

if 'djcelery' in settings.INSTALLED_APPS:
	CELERY_IS_ACTIVE = True
	from djcelery.models import TaskMeta
	from core.tasks import async_move_pages, async_add_category, async_move_category, \
			async_remove_category, async_add_internal_link, async_sub
else:
	CELERY_IS_ACTIVE = False

from core.utils import make_messages, method_restricted_to, is_ajax
from core.handlers import wiki_handler
w = wiki_handler()

@method_restricted_to('GET')
def index(request):
    return render(request, 'index.html', {
        'title':'ZuluBot',
		'CELERY_IS_ACTIVE':CELERY_IS_ACTIVE
    })

@is_ajax()
@method_restricted_to('GET')
def search_page(request):
    if request.GET.get('type','content') == 'content':
        results = [ p for p in w.search_words(request.GET['q']) ]
    else:
        results = [ p for p in \
            w.search_in_title(request.GET['q'], namespaces=request.GET.get('type',None)) ]
    
    return render(request, 'option.html', {
        'pages':results,
    })

@is_ajax()
@method_restricted_to('POST')
def move_page(request):
    w.move_page(request.POST['from'], request.POST['to'])
    messages.add_message(request, messages.INFO, 'Action en cours.',
                                 fail_silently=True)
    return render(request, 'base/messages.html', {
        'messages':messages.get_messages(request),
    })

@is_ajax()
@method_restricted_to('POST')
def move_pages(request):
    pages = request.POST.getlist('pages[]')
    if len(pages) > 1 and CELERY_IS_ACTIVE :
        async_move_pages.delay(pages, request.POST['from'], request.POST['to'], request.POST['redirect'])
        messages.add_message(request, messages.INFO, 'Renommage en cours.')
        msgs = messages.get_messages(request)
    else:
        results = w.move_pages(pages, request.POST['from'], request.POST['to'], request.POST['redirect'])
        msgs = make_messages(request, results)

    return render(request, 'base/messages.html', {
        'messages':msgs,
    })

@is_ajax()
@method_restricted_to('GET')
def check_page(request):
    p = w.get_page(request.GET['page'])
    if p.exists():
        messages.add_message(request, messages.SUCCESS, 'Correcte.')
    else:
        messages.add_message(request, messages.WARNING, 'Introuvable.')
    return render(request, 'base/messages.html', {
        'messages':messages.get_messages(request),
    })
    
@is_ajax()
@method_restricted_to('POST')
def add_category(request):
    pages = request.POST.getlist('pages[]')
    if CELERY_IS_ACTIVE :
        async_add_category.delay(pages, request.POST['category'])
        messages.add_message(request, messages.INFO, u'Ajout de cat\xe9gorie en cours.')
        msgs = messages.get_messages(request)
    else:
        results = w.add_category(pages, request.POST['category'])
        msgs = make_messages(request, results)

    return render(request, 'base/messages.html', {
        'messages':msgs,
    })

@is_ajax()
@method_restricted_to('POST')
def move_category(request):
    if CELERY_IS_ACTIVE :
        async_move_category.delay(request.POST['from'], request.POST['to'])
        messages.add_message(request, messages.INFO, u'D\xe9placement de cat\xe9gorie en cours.')
    else:
        w.move_category(request.POST['from'], request.POST['to'])
        messages.add_message(request, messages.INFO, u'D\xe9placement de cat\xe9gorie termin\xe9.'),
    return render(request, 'base/messages.html', {
        'messages':messages.get_messages(request),
    })

@is_ajax()
@method_restricted_to('POST')
def remove_category(request):
    pages = request.POST.getlist('pages[]')
    if CELERY_IS_ACTIVE :
        async_remove_category.delay(pages, request.POST['category'])
        messages.add_message(request, messages.INFO, u'Suppression de cat\xe9gorie en cours.')
        msgs = messages.get_messages(request)
    else:
        w.remove_category(pages, request.POST['category'])
        messages.add_message(request, messages.INFO, u'D\xe9placement de cat\xe9gorie termin\xe9.'),
        msgs = make_messages(request, results)

    return render(request, 'base/messages.html', {
        'messages':messages.get_messages(request),
    })

@is_ajax()
@method_restricted_to('POST')
def add_internal_link(request):
    pages = request.POST.getlist('pages[]')
    if CELERY_IS_ACTIVE :
        async_add_internal_link.delay(pages, request.POST['link'], request.POST['link_text'])
        messages.add_message(request, messages.INFO, u"Ajout d'hyperliens en cours.")
    else:
        results = w.add_internal_link(pages, request.POST['link'], request.POST['link_text'])
        msgs = make_messages(request, results)

    return render(request, 'base/messages.html', {
        'messages':messages.get_messages(request),
    })

@is_ajax()
@method_restricted_to('POST')
def sub(request):
    pages = request.POST.getlist('pages[]')
    if CELERY_IS_ACTIVE :
        async_sub.delay(pages, request.POST['from'], request.POST['to'])
        messages.add_message(request, messages.INFO, u"Subtitution de texte en cours.")
    else:
        results = w.sub(pages, request.POST['from'], request.POST['to'])
        msgs = make_messages(request, results)

    return render(request, 'base/messages.html', {
        'messages':messages.get_messages(request),
    })

@is_ajax()
@method_restricted_to('GET')
def get_finished_tasks(request):
    if not CELERY_IS_ACTIVE:
        raise Http404
    results = [ t.result  for t in TaskMeta.objects.all() ]
    [ t.delete()  for t in TaskMeta.objects.filter(status='SUCCESS') ]
    return render(request, 'base/messages.html', {
        'messages':make_messages(request, results),
    })
