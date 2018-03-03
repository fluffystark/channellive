from django.conf.urls import url

from django.conf.urls import include


urlpatterns = [
    url(r'^logging/', include('rest_framework.urls')),
]
