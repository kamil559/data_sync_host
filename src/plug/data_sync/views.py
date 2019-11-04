from django.conf import settings
from django.core.cache import caches
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from data_sync.utils import get_current_timestamp


class HealthCheck(APIView):

    def get(self, request):
        return Response(status=status.HTTP_200_OK)


class TimestampSync(APIView):

    def get(self, request, unique_id):
        current_timestamp = get_current_timestamp()

        if unique_id is not None:
            caches["default"].set(unique_id, current_timestamp, timeout=settings.CACHE_TTL)

        return Response(data={"timestamp": current_timestamp}, status=status.HTTP_200_OK)


