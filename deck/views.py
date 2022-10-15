from django.http import HttpResponse
from django.shortcuts import render
from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.generics import CreateAPIView
from rest_framework.parsers import FormParser, MultiPartParser, JSONParser
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.utils import json

from deck.deck_serializer import DeckCreateSerializer, DeckResponseTemplateSerializer, DeckRequestTemplateSerializer
from deck.folder_serializers import FolderCreateSerializer
from deck.forms import DeckCreateForm


class DeckCreateView(CreateAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = DeckCreateSerializer

    def createPostResponse(self, deck):
        cards = deck.card_set.all()
        response_data = deck.__dict__
        response_data['cards'] = []
        for card in cards:
            response_data['cards'].append(card.__dict__)
        deck_serializer = DeckResponseTemplateSerializer(data=response_data)
        if deck_serializer.is_valid():
            return Response(deck_serializer.data, status=status.HTTP_201_CREATED)

        return Response(deck_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @extend_schema(
        request=DeckRequestTemplateSerializer,
        responses={
            200: DeckResponseTemplateSerializer,
            400: None
        }
    )
    def post(self, request, *args, **kwargs):
        user = request.user
        serializer = self.serializer_class(data=json.loads(request.data['data']))
        if serializer.is_valid():
            serializer.save(author_id=user.id, files=request.data)
            return self.createPostResponse(serializer.instance)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class FolderCreateView(CreateAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = FolderCreateSerializer

    @extend_schema(
        responses={
            200: FolderCreateSerializer,
            400: None
        }
    )
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save(files=request.files)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
