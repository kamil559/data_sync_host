from django.urls import path

from data_sync.views import HealthCheck, TimestampSync

urlpatterns = [
    path('health-check', HealthCheck.as_view(), name="health_check"),
    path('timestamp-sync/<uuid:unique_id>', TimestampSync.as_view(), name="timestamp_sync")
]
