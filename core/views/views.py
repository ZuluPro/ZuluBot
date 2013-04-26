from django.shortcuts import render

from core.views import CELERY_IS_ACTIVE
from core.models import Wiki_User, Wiki_User_Form
from core.utils import method_restricted_to, is_ajax
from core.handlers import wiki_handler

@method_restricted_to('GET')
def index(request):
    # TODO
    # Handling wiki ValueError
    try:
        w = wiki_handler()
    except Wiki_User.NoActiveUser:
        w = None

    return render(request, 'index.html', {
        'title':'ZuluBot',
        'w':w,
        'wiki_user_form':Wiki_User_Form(),
        'Users':Wiki_User.objects.all(),
        'F':Wiki_User_Form(),
        'CELERY_IS_ACTIVE':CELERY_IS_ACTIVE
    })

@is_ajax()
@method_restricted_to('POST')
def get_page_links(request):
    page_names = request.POST.getlist('pages[]')

    return render(request, 'base/messages.html', {
        'messages':msgs,
    })

@is_ajax()
@method_restricted_to('GET')
def search_contrib(request):
    w = wiki_handler()
    contribs = w.get_contrib()
    if request.GET.get('q',''):
        contribs = [ (p,i,d,c) for p,i,d,c in contribs if request.GET['q'] in p.title() ]
    return render(request, 'contrib/li.html', {
        'crontribs':contribs,
    })

