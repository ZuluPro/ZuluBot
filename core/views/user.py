from django.http import Http404
from django.shortcuts import render, redirect
from django.contrib import messages
from django.conf import settings

from core.models import Wiki_User, Wiki_User_Form
from core.utils import method_restricted_to, is_ajax
from core.handlers import wiki_handler
w = wiki_handler()

@is_ajax()
@method_restricted_to('POST')
def add_user(request):
    F = Wiki_User_Form(request.POST)
    if F.is_valid():
        pass
    else:
        pass

@is_ajax()
@method_restricted_to('POST')
def get_user(request):
    F = Wiki_User_Form(request.POST)
    return render(request, 'contrib/li.html', {
        'F':F,
    })
