from django.conf.urls import include, url
from rest_framework.routers import DefaultRouter

from EventHandler import views

router = DefaultRouter()
router.register(r'events', views.EventViewSet)

urlpatterns = [
    url(r'^', include(router.urls)),
]
