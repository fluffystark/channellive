from django.conf.urls import include, url
from rest_framework.routers import DefaultRouter

from FileUpload import views

router = DefaultRouter()
router.register(r'file', views.FileUploadViewSet, base_name='file')

urlpatterns = [
    url(r'^', include(router.urls)),
]
