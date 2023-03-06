import datetime

from django.http import HttpResponse
from drf_spectacular.utils import inline_serializer, OpenApiResponse, extend_schema
from rest_framework import viewsets, fields, status
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework_api_key.permissions import HasAPIKey

from analytic.helpers import get_user_analytic, add_event
from analytic.models import EventsCategoryModel, EventsModel
from analytic.serializers import AppLaunchSerializer
from studyhub.settings import logger


class EventsViewSet(viewsets.ViewSet):
    permission_classes = [HasAPIKey]

    @extend_schema(
        request=inline_serializer("AppLaunchRequest",
                                  {"platform": fields.CharField(),
                                   "ipAddress": fields.CharField()}),
        responses={
            200: 'App launch details successfully added',
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
        return Response("App launch details successfully added", status=200)

    @extend_schema(
        responses={
            200: 'Event successfully added',
            (400, 'text/plain'): OpenApiResponse(description="Some fields do not correct")
        }
    )
    def app_on_background(self, request):
        add_event(request.user, EventsCategoryModel.objects.get(event_category_name='App on background'))
        return Response("Event successfully added", status=200)

    @extend_schema(
        responses={
            200: 'Event successfully added',
            (400, 'text/plain'): OpenApiResponse(description="Some fields do not correct")
        }
    )
    def app_closed(self, request):
        add_event(request.user, EventsCategoryModel.objects.get(event_category_name='App closed'))
        return Response("Event successfully added", status=200)
