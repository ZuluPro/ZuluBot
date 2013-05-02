from django.http import Http404
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages

from core.models import Wiki_User, Wiki_User_Form
from core.utils import method_restricted_to, is_ajax, Task_Result
from core.handlers import wiki_handler


@is_ajax()
@method_restricted_to('POST')
def add_user(request):
    results = Task_Result()
    F = Wiki_User_Form(data=request.POST)
    if F.is_valid():
        F.save()
        results.add_result('success', u'Utilisateur ajout\xe9.')
    else:
        for field, err in F.errors.items():
            results.add_result('error', '<b>%s:</b> %s' % (field, err))

    return render(request, 'base/messages.html', {
        'messages': results.make_messages(request),
    })


@is_ajax()
@method_restricted_to('POST')
def update_user(request):
    U = get_object_or_404(Wiki_User.objects.filter(id=request.POST['id']))
    results = Task_Result()
    F = Wiki_User_Form(data=request.POST, instance=U)
    if F.is_valid():
        U = F.save()
        results.add_result('success', u'Utilisateur modifi\xe9.')
    else:
        for field, err in F.errors.items():
            results.add_result('error', '<b>%s:</b> %s' % (field, err))

    return render(request, 'base/messages.html', {
        'messages': results.make_messages(request),
    })


@is_ajax()
@method_restricted_to('GET')
def get_user(request):
    if 'id' in request.GET:
        U = get_object_or_404(Wiki_User.objects.filter(id=request.GET['id']))
        F = Wiki_User_Form(instance=U)
    else:
        F = Wiki_User_Form()

    return render(request, 'user_form.html', {
        'F': F,
    })


@is_ajax()
@method_restricted_to('GET')
def get_user_list(request):
    Us = Wiki_User.objects.all()
    return render(request, 'user_list.html', {
        'Users': Us,
    })


@is_ajax()
@method_restricted_to('POST')
def delete_user(request):
    U = get_object_or_404(Wiki_User.objects.filter(id=request.POST['id']))
    U.delete()
    return render(request, 'user_list.html', {
        'Users': Wiki_User.objects.all(),
    })


@is_ajax()
@method_restricted_to('POST')
def set_active_user(request):
    U = get_object_or_404(Wiki_User.objects.filter(id=request.POST['id']))
    U.set_active()
    results = Task_Result()
    results.add_result('warning', u'Utilisateur actif modifi\xe9.<br>La page va \xeatre recharg\xe9e.')
    return render(request, 'base/messages.html', {
        'messages': results.make_messages(request),
    })
