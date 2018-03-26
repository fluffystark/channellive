from django.conf.urls import include, url
from rest_framework.routers import DefaultRouter

from OpenTokHandler import views

router = DefaultRouter()
router.register(r'livestream', views.LivestreamViewSet, base_name='livestream')
router.register(r'subscribe', views.SubscriberViewSet, base_name='subscribe')
router.register(r'vote', views.VoteViewSet, base_name='vote')
router.register(r'archive', views.ArchiveViewSet, base_name='archive')

urlpatterns = [
    url(r'^', include(router.urls)),
]
