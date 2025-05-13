from django.conf.urls.static import static
from rest_framework.routers import DefaultRouter

from config import settings
from trackers.apps import TrackersConfig
from trackers.views import TrackerViewSet


app_name = TrackersConfig.name


router = DefaultRouter()
router.register("trackers", TrackerViewSet, basename="trackers")

urlpatterns = [] + router.urls

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)