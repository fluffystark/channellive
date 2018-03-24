from django.conf.urls import include, url
from rest_framework.routers import DefaultRouter

from event import views

router = DefaultRouter()
router.register(r'categories', views.CategoryViewSet, base_name='categories')
router.register(r'events', views.EventViewSet, base_name='events')
router.register(r'hasevent', views.HasEventViewSet, base_name='hasevent')
router.register(r'file', views.FileUploadViewSet, base_name='file')
router.register(r'prizes', views.PrizeViewSet, base_name='prizes')

urlpatterns = [
    url(r'^', include(router.urls)),
]
