from django.conf.urls import url

from rest_framework.authtoken import views as authviews


urlpatterns = [
    url(r'^api-token-auth/', authviews.obtain_auth_token)
]
