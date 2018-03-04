"""channellive URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin
from rest_framework.routers import DefaultRouter

# from EventHandler import views as eventview
from OpenTokHandler import views as tokview
# from UserProfile import views as userview
from django.conf.urls.static import static
from channellive import settings


from EventHandler.urls import router as eventRouter
from UserProfile.urls import router as userRouter
# separate url to their own apps

router = DefaultRouter()
router.registry.extend(eventRouter.registry)
router.registry.extend(userRouter.registry)


urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^', include(router.urls)),
    url(r'^api-auth/', include('rest_framework.urls')),
    url(r'^opentok/$', tokview.OpenTokView.as_view(), name='opentok'),
]
if settings.DEBUG is True:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
