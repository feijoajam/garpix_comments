from garpixcms.urls import *  # noqa

from django.urls import path
from garpix_auth.views import LogoutView, LoginView
from django.conf import settings

API_URL = getattr(settings, 'API_URL', 'api')

urlpatterns = [
                  path(f'{API_URL}/', include('garpix_comments.urls'))  # noqa: F405
              ] + urlpatterns  # noqa
