from django.conf.urls import include, url
from rest_framework.routers import DefaultRouter

from OpenTokHandler import views

router = DefaultRouter()
router.register(r'livestream', views.LivestreamViewSet, base_name='livestream')
router.register(r'livestream/end', views.EndStreamViewSet, base_name='endlivestream')
router.register(r'livestream/status', views.ArchiveViewSet, base_name='livestreamStatus')
router.register(r'subscribe', views.SubscriberViewSet, base_name='subscribe')
router.register(r'vote', views.VoteViewSet, base_name='vote')

urlpatterns = [
    url(r'^', include(router.urls)),
]
