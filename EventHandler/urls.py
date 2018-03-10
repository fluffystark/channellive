from django.conf.urls import include, url
from rest_framework.routers import DefaultRouter

from EventHandler import views

router = DefaultRouter()
router.register(r'events', views.EventViewSet)
router.register(r'categories', views.CategoryViewSet)

urlpatterns = [
    url(r'^', include(router.urls)),
]
