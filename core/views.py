from django.shortcuts import render, redirect
from django.contrib import messages
from zulubot.handlers import wiki_handler
w = wiki_handler()

def index(request):
    return render(request, 'index.html', {
        'title':'ZuluBot',
    })

def search_page(request):
    s1 = [ p for p in w.search_words(request.GET['q']) ]
    s2 = w.search_in_title(request.GET['q'])
    s = list(set(s1 + s2))
    
    return render(request, 'option.html', {
        'pages':s,
    })

def move_page(request):
    w.move_page(request.POST['from'], request.POST['to'])
    messages.add_message(request, messages.INFO, 'Action en cours.',
                                 fail_silently=True)
    return render(request, 'base/messages.html', {
        'messages':messages.get_messages(request),
    })

def move_pages(request):
    w.move_pages(request.POST.getlist('pages[]'), request.POST['from'], request.POST['to'], request.POST['redirect'])
    messages.add_message(request, messages.INFO, 'Action en cours.',
                                 fail_silently=True)
    return render(request, 'base/messages.html', {
        'messages':messages.get_messages(request),
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
    w.add_category(request.POST.getlist('pages[]'), request.POST['category'])
    messages.add_message(request, messages.INFO, 'Action en cours.',
                                 fail_silently=True)
    return render(request, 'base/messages.html', {
        'messages':messages.get_messages(request),
    })

def move_category(request):
    w.move_category('from', request.POST['to'])
    messages.add_message(request, messages.INFO, 'Action en cours.',
                                 fail_silently=True)
    return render(request, 'base/messages.html', {
        'messages':messages.get_messages(request),
    })

