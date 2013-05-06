from django.shortcuts import render

from core.views import CELERY_IS_ACTIVE
from core.models import Wiki_User, Wiki_User_Form
from core.utils import method_restricted_to, is_ajax
from core.handlers import wiki_handler


@method_restricted_to('GET')
def index(request):
    """
    Index of website.
    This is the only view which is not AJAX.
    """
    # TODO
    # Handling wiki ValueError
    try:
        w = wiki_handler()
    except Wiki_User.NoActiveUser:
        w = None

    return render(request, 'index.html', {
        'title': 'ZuluBot',
        'w': w,
        'wiki_user_form': Wiki_User_Form(),
        'Users': Wiki_User.objects.all(),
        'F': Wiki_User_Form(),
        'CELERY_IS_ACTIVE': CELERY_IS_ACTIVE
    })


@is_ajax()
@method_restricted_to('GET')
def search_contrib(request):
    """
    DO NOT USE
    """
    w = wiki_handler()
    contribs = w.get_contrib()
    if request.GET.get('q', ''):
        contribs = [ (p, i, d, c) for p, i, d, c in contribs if request.GET['q'] in p.title() ]
    return render(request, 'contrib/li.html', {
        'crontribs': contribs,
    })


@method_restricted_to('GET')
def apropos(request):
    from django.conf import settings
    with open(settings.BASEDIR+'/../LICENSE') as license_file:
        license = license_file.read()
    return render(request, 'apropos.html', {
        'license': license,
    })
