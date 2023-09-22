from garpixcms.urls import *  # noqa

from django.urls import path, include
from django.conf import settings

API_URL = getattr(settings, 'API_URL', 'api')

urlpatterns = \
    [
        path('', include(('garpix_comments.urls', 'comments'), namespace='garpix_comments')),
        path('', include(('testapp.urls', 'testapp'), namespace='testapp')),
    ] + urlpatterns  # noqa
