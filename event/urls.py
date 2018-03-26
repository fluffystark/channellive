from django.conf.urls import include, url
from rest_framework.routers import DefaultRouter

from event import views

router = DefaultRouter()
router.register(r'categories', views.CategoryViewSet, base_name='categories')
router.register(r'events', views.EventViewSet, base_name='events')
router.register(r'hasevent', views.HasEventViewSet, base_name='hasevent')
router.register(r'event_file', views.EventImageViewSet, base_name='event_file')
router.register(r'prizes', views.PrizeViewSet, base_name='prizes')
router.register(r'upload', views.ImageViewSet, base_name='upload')

urlpatterns = [
    url(r'^', include(router.urls)),
]
