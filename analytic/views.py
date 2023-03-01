from django.http import HttpResponse
from drf_spectacular.utils import inline_serializer, OpenApiResponse, extend_schema
from rest_framework import viewsets, fields, status
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework_api_key.permissions import HasAPIKey

from analytic.serializers import AppLaunchSerializer
from studyhub.settings import logger


class UserPropertiesViewSet(viewsets.ViewSet):
    permission_classes = [HasAPIKey]

    @extend_schema(
        request=inline_serializer("AppLaunchRequest",
                                  {"platform": fields.CharField(),
                                   "ipAddress": fields.CharField()}),
        responses={
            200: '',
            (400, 'text/plain'): OpenApiResponse(description="Some fields do not correct")
        }
    )
    def app_launch(self, request):
        user = request.user

        platform = request.data.get('platform', None)
        ip_address = request.data.get('ipAddress', None)

        serializer_data = {
            'platform': platform,
            'ip_address': ip_address,
        }
        if user.is_authenticated:
            serializer_data['user_id'] = user.id

        serializer = AppLaunchSerializer(data=serializer_data)

        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        serializer.save()
        return Response(status=200)


