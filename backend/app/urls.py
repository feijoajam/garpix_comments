from garpixcms.urls import *  # noqa

from django.urls import path
from garpix_auth.views import LogoutView, LoginView
from django.conf import settings

API_URL = getattr(settings, 'API_URL', 'api')

urlpatterns = [
                path('', include(('garpix_comments.urls', 'comments'), namespace='garpix_comments')),
              ] + urlpatterns  # noqa
