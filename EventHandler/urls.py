from django.conf.urls import include, url
from rest_framework.routers import DefaultRouter

from EventHandler import views

router = DefaultRouter()
router.register(r'events', views.EventViewSet, base_name='events')
router.register(r'categories', views.CategoryViewSet, base_name='categories')
router.register(r'hasevent', views.HasEventViewSet, base_name='hasevent')

urlpatterns = [
    url(r'^', include(router.urls)),
]
