from django.conf import settings
from django.urls import path, include

from .routers import router

app_name = 'testapp'

urlpatterns = [
    path(f'{settings.API_URL}/', include(router.urls))
]
