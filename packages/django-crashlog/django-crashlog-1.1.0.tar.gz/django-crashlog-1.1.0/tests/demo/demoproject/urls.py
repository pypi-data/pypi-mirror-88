# import adminactions.urls
from django.contrib.admin import autodiscover, site
from django.contrib.auth.decorators import login_required
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.http import HttpResponse
from django.urls import include, path

from crashlog.middleware import process_exception

autodiscover()


def raise_error(request):
    raise IndexError('IndexError')


@login_required
def raise_with_message_user(request):
    try:
        raise IndexError('IndexError')
    except Exception as e:
        process_exception(e, request, message_user=True)
    return HttpResponse()


urlpatterns = [path('/raise-error', raise_error, name='raise-error'),
               path('/raise_with_message_user', raise_with_message_user, name='raise_with_message_user'),
               path('', site.urls),
               ] + staticfiles_urlpatterns()
