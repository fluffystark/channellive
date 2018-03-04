from django.conf.urls import include, url
from rest_framework.routers import DefaultRouter

from UserProfile import views

router = DefaultRouter()
router.register(r'register', views.UserViewSet)
router.register(r'login', views.LoginViewSet)
router.register(r'business', views.BusinessViewSet)

urlpatterns = [
    url(r'^', include(router.urls)),
]
