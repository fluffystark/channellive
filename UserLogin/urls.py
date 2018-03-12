from django.conf.urls import include, url
from rest_framework.routers import DefaultRouter

from UserLogin import views

router = DefaultRouter()
router.register(r'login', views.LoginViewSet, base_name='login')

urlpatterns = [
    url(r'^', include(router.urls)),
]
