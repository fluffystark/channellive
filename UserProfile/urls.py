from django.conf.urls import include, url
from rest_framework.routers import DefaultRouter

from UserProfile import views

router = DefaultRouter()
router.register(r'business', views.BusinessViewSet, base_name='business')

urlpatterns = [
    url(r'^', include(router.urls)),
]
