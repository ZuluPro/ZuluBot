"""
All this views work only with AJAX.
If request isn't return a HTML 404.

Views' methods are also restricted to
their functions, so they return 404 too
if method isn't appropriate.
"""

from django.http import Http404
from django.shortcuts import render, redirect
from django.contrib import messages

from core.views import CELERY_IS_ACTIVE
from core.utils import method_restricted_to, is_ajax
from core.handlers import wiki_handler

@is_ajax()
@method_restricted_to('GET')
def search_page(request):
    """
    Return a list of page with <option>.
    request['q'] is a search string.
    request['type'] is the type of request:
     - An integer for namespace
     - String 'content' for search in content
    """
    w = wiki_handler()
    # By default search in words
    if request.GET.get('type','content') == 'content':
        results = [ p for p in w.search_words(request.GET['q']) ]
    elif request.GET['type'] == 'references':
        page = w.get_page(request.GET['q'])
        results = page.getReferences()
    # Else search by namespace and name
    else:
        results = [ p for p in \
            w.search_in_title(request.GET['q'], namespaces=request.GET.get('type',None)) ]
    
    return render(request, 'option.html', {
        'pages':results,
    })

@is_ajax()
@method_restricted_to('POST')
def move_page(request):
    """
    Move content of a page to another.
    This view isn't purpose in HTML.
    """
    w = wiki_handler()
    w.move_page(request.POST['from'], request.POST['to'])
    messages.add_message(request, messages.INFO, 'Action en cours.')
    return render(request, 'base/messages.html', {
        'messages':messages.get_messages(request),
    })

@is_ajax()
@method_restricted_to('POST')
def move_pages(request):
    """
    Rename list of pages with request's keys.
    It uses 'pat' 'repl' as re.sub with regex.

    This view use Celery if it's actived and there
    are more than one page to rename.
    """
    pages = request.POST.getlist('pages[]')
    if len(pages) > 1 and CELERY_IS_ACTIVE :
        async_move_pages.delay(pages, request.POST['pat'], request.POST['repl'], request.POST['redirect'])
        messages.add_message(request, messages.INFO, 'Renommage en cours.')
        msgs = messages.get_messages(request)
    else:
        w = wiki_handler()
        results = w.move_pages(pages, request.POST['pat'], request.POST['repl'], request.POST['redirect'])
        msgs = results.make_messages(request)

    return render(request, 'base/messages.html', {
        'messages':msgs,
    })

@is_ajax()
@method_restricted_to('GET')
def check_page(request):
    """
    Check if page exists and return appropriate message.
    """
    w = wiki_handler()
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
    """
    Add category to a list of pages.
    This view use Celery if it's actived.
    """
    pages = request.POST.getlist('pages[]')
    if CELERY_IS_ACTIVE :
        async_add_category.delay(pages, request.POST['category'])
        messages.add_message(request, messages.INFO, u'Ajout de cat\xe9gorie en cours.')
        msgs = messages.get_messages(request)
    else:
        w = wiki_handler()
        results = w.add_category(pages, request.POST['category'])
        msgs = results.make_messages(request)

    return render(request, 'base/messages.html', {
        'messages':msgs,
    })

@is_ajax()
@method_restricted_to('POST')
def move_category(request):
    """
    Rename category.
    This view use Celery if it's actived.
    """
    if CELERY_IS_ACTIVE :
        async_move_category.delay(request.POST['from'], request.POST['to'])
        messages.add_message(request, messages.INFO, u'D\xe9placement de cat\xe9gorie en cours.')
    else:
        w = wiki_handler()
        w.move_category(request.POST['from'], request.POST['to'])
        messages.add_message(request, messages.INFO, u'D\xe9placement de cat\xe9gorie termin\xe9.'),
    return render(request, 'base/messages.html', {
        'messages':messages.get_messages(request),
    })

@is_ajax()
@method_restricted_to('POST')
def remove_category(request):
    """
    Remove category from a list of pages.
    This view use Celery if it's actived.
    """
    pages = request.POST.getlist('pages[]')
    if CELERY_IS_ACTIVE :
        async_remove_category.delay(pages, request.POST['category'])
        messages.add_message(request, messages.INFO, u'Enl\xe8vement de cat\xe9gorie en cours.')
        msgs = messages.get_messages(request)
    else:
        w = wiki_handler()
        results.remove_category(pages, request.POST['category'])
        messages.add_message(request, messages.INFO, u'Enl\xe8vement de cat\xe9gorie termin\xe9.'),
        msgs = results.make_messages(request)

    return render(request, 'base/messages.html', {
        'messages':messages.get_messages(request),
    })

@is_ajax()
@method_restricted_to('POST')
def add_internal_link(request):
    """
    Modify page's text for add internal links for the given string.
    A text link can be given with request['link_test']
    This view use Celery if it's actived.
    """
    pages = request.POST.getlist('pages[]')
    if CELERY_IS_ACTIVE :
        async_add_internal_link.delay(pages, request.POST['link'], request.POST['link_text'])
        messages.add_message(request, messages.INFO, u"Ajout d'hyperliens en cours.")
    else:
        w = wiki_handler()
        results = w.add_internal_link(pages, request.POST['link'], request.POST['link_text'])
        msgs = results.make_messages(request)

    return render(request, 'base/messages.html', {
        'messages':messages.get_messages(request),
    })

@is_ajax()
@method_restricted_to('POST')
def sub(request):
    """
    Make a simple text subsitution in pages' text.
    This view use Celery if it's actived.
    """
    pages = request.POST.getlist('pages[]')
    if CELERY_IS_ACTIVE :
        async_sub.delay(pages, request.POST['from'], request.POST['to'])
        messages.add_message(request, messages.INFO, u"Subtitution de texte en cours.")
    else:
        w = wiki_handler()
        results = w.sub(pages, request.POST['from'], request.POST['to'])
        msgs = results.make_messages(request)

    return render(request, 'base/messages.html', {
        'messages':messages.get_messages(request),
    })

@is_ajax()
@method_restricted_to('GET')
def get_page_links(request):
    """
    Return a list of link to wiki's page.
    """
    w = wiki_handler()
    page_names = request.GET.getlist('pages[]')
    results = w.get_pages_wiki_url(page_names)
    msgs = results.make_messages(request, header='Hyperliens:')

    return render(request, 'base/messages.html', {
        'messages':msgs,
    })

@is_ajax()
@method_restricted_to('GET')
def get_finished_tasks(request):
    """
    Control of Celery's asynchronous tasks.
    This view return a 404 if Celery is unactived.
    It's normally requested by a Javascript loop.
    """
    if not CELERY_IS_ACTIVE:
        raise Http404
    # Extract Celery result
    task_results = [ t.result  for t in TaskMeta.objects.all() ]
    # Create list messages objects
    msgs_groups = [ t.make_messages(request) for t in task_results ]
    # Delete finished task
    [ t.delete()  for t in TaskMeta.objects.filter(status='SUCCESS') ]

    msgs = []
    for group in msgs_groups:
        msgs += [ m for m in group ]
    return render(request, 'base/messages.html', {
        'messages':msgs
    })

