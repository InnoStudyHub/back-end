import logging

from django.views.decorators.csrf import csrf_exempt
from drf_spectacular.utils import extend_schema, inline_serializer, OpenApiResponse
from rest_framework import status, viewsets, fields
from rest_framework.exceptions import ValidationError, NotFound
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.utils import json

from deck.helpers.deck_helpers import logger, getDeckData, getDecks
from deck.serializers.deck_serializer import DeckCreateSerializer, DeckRequestSerializer, \
    DeckListSerializer, DeckDetailSerializer, DeckPreviewSerializer
from deck.serializers.folder_serializers import FolderCreateSerializer, FolderDetailSerializer
from deck.models import Deck, Folder

class DeckViewSet(viewsets.ViewSet):
    permission_classes = (IsAuthenticated,)

    @extend_schema(
        description='Create deck request',
        request=DeckRequestSerializer,
        responses={
            201: DeckDetailSerializer,
            (400, 'text/plain'): OpenApiResponse(description="Some fields is not exist"),
            (403, 'text/plain'): OpenApiResponse(description="Deck with this name exist")
        }
    )
    def create(self, request):
        user = request.user
        logger.info(f"Handle deck create request: {request.data}, from user {user.id}")
        data = json.loads(request.data['data'])
        serializer = DeckCreateSerializer(data=data)
        if serializer.is_valid(raise_exception=True):
            serializer.save(author_id=user.id, files=request.data)
            response_data = getDeckData(serializer.instance, user)
            return Response(response_data, status=status.HTTP_201_CREATED)
        else:
            logger.warning("Something wrong with request body")
            raise ValidationError(serializer.error_messages)

    def createFromGoogleSheet(self, request):
        user = request.user
        logger.info(f"Handle deck create request: {request.data}, from user {user.id}")
        data = json.loads(request.data['data'])
        serializer = DeckCreateSerializer(data=data)
        if serializer.is_valid(raise_exception=True):
            serializer.save(author_id=user.id)
            response_data = getDeckData(serializer.instance, user)
            return Response(response_data, status=status.HTTP_201_CREATED)
        else:
            logger.warning("Something wrong with request body")
            raise ValidationError(serializer.error_messages)

    @extend_schema(
        description='Get deck by id',
        request=inline_serializer("GetDeckById", {"deck_id": fields.IntegerField()}, many=False),
        responses={
            200: DeckDetailSerializer
        }
    )
    def get_by_id(self, request):
        user = request.user

        if not request.data.get('deck_id'):
            raise ValidationError("field deck_id does not exist")

        deck_id = request.data['deck_id']

        if not Deck.objects.all().filter(deck_id=deck_id).exists():
            raise NotFound(f"Deck with id-{deck_id} does not exist")

        deck_data = getDeckData(Deck.objects.get(deck_id=deck_id), user)
        return Response(deck_data, status=status.HTTP_200_OK)

    @extend_schema(
        description='Get user deck by name',
        request=inline_serializer("GetDeckByName", {"deck_name": fields.CharField()}, many=False),
        responses={
            200: DeckDetailSerializer
        }
    )
    def get_by_name(self, request):
        user = request.user

        if not request.data.get('deck_name'):
            raise ValidationError("field deck_name does not exist")
        if not request.data.get('folder_id'):
            raise ValidationError("field folder_id does not exist")

        deck_name = request.data['deck_name']
        folder_id = request.data['folder_id']

        if not Folder.objects.filter(folder_id=folder_id).exists():
            raise NotFound(f"Folder with folder_id={folder_id} does not exist")
        if not user.deck_set.filter(deck_name=deck_name, folder_id=folder_id).exists():
            raise NotFound(f"User deck with name={deck_name} and folder_id={folder_id} does not exist")

        deck = user.deck_set.get(deck_name=deck_name, folder_id=folder_id)
        return Response(getDeckData(deck, user), status=status.HTTP_200_OK)


class FolderViewSet(viewsets.ViewSet):
    permission_classes = (IsAuthenticated,)

    @extend_schema(
        request=FolderCreateSerializer,
        responses={
            201: FolderCreateSerializer,
            (400, 'text/plain'): OpenApiResponse(description="Some fields is not exist")
        }
    )
    def create(self, request, *args, **kwargs):
        serializer = FolderCreateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @extend_schema(
        responses={
            200: FolderDetailSerializer(many=True)
        }
    )
    def list(self, request, *args, **kwargs):
        folders = Folder.objects.all()
        folders_data = []
        for folder in folders:
            folders_data.append({"folder_name": folder.folder_name, "folder_id": folder.id})
        return Response(folders_data, status=status.HTTP_200_OK)
