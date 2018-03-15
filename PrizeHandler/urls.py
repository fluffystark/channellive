from django.conf.urls import include, url
from rest_framework.routers import DefaultRouter

from PrizeHandler import views

router = DefaultRouter()
router.register(r'prizes', views.PrizeViewSet, base_name='prizes')

urlpatterns = [
    url(r'^', include(router.urls)),
]
