from django.conf.urls import include, url
from rest_framework.routers import DefaultRouter

from UserProfile import views

router = DefaultRouter()
router.register(r'users', views.UserViewSet)

urlpatterns = [
    url(r'^', include(router.urls)),
    url(r'^login/$', views.LoginView.as_view(), name='login'),
]
