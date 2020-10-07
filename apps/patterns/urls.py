from django.conf.urls import url
from rest_framework.routers import DefaultRouter
from apps.patterns.views import OcurrenceViewSet

router = DefaultRouter()
router.register(r'ocurrences', OcurrenceViewSet, basename="ocurrences")
urlpatterns = router.urls
