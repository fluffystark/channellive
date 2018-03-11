from django.conf.urls import include, url
from rest_framework.routers import DefaultRouter

from UserRegistration import views

router = DefaultRouter()
router.register(r'register', views.UserRegistrationViewSet)

urlpatterns = [
    url(r'^', include(router.urls)),
]
