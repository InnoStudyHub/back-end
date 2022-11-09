import logging

from drf_spectacular.utils import extend_schema, inline_serializer, OpenApiResponse
from rest_framework import status, viewsets, fields
from rest_framework.exceptions import ValidationError, NotFound
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.utils import json

from deck.serializers.deck_serializer import DeckCreateSerializer, DeckRequestSerializer, \
    DeckListSerializer, DeckDetailSerializer, DeckPreviewSerializer
from deck.serializers.folder_serializers import FolderCreateSerializer, FolderDetailSerializer
from deck.models import Deck, Folder

logger = logging.getLogger(__name__)


def getDeckData(deck, user):
    logger.info("Try to create DeckData")
    cards = deck.card_set.all()
    data = deck.__dict__
    data['cards'] = []
    data['is_favourite'] = user.favourite_decks.contains(deck)
    for card in cards:
        data['cards'].append(card.__dict__)
    serializer = DeckDetailSerializer(data=data)
    if not serializer.is_valid(raise_exception=True):
        raise ValidationError(serializer.error_messages)
    logger.info(f"DeckData successfully created: {serializer.data}")
    return serializer.data


def getDeckPreview(deck, user):
    logger.info("Try to create DeckDataPreview")
    cards = deck.card_set.all()
    data = deck.__dict__
    data['cards'] = len(cards)
    data['is_favourite'] = user.favourite_decks.contains(deck)
    serializer = DeckPreviewSerializer(data=data)
    if not serializer.is_valid(raise_exception=True):
        raise ValidationError(serializer.error_messages)
    logger.info(f"DeckDataPreview successfully created: {serializer.data}")
    return serializer.data


def getDecks(filter):
    return Deck.objects.all().filter(**filter)


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

    @extend_schema(
        description='Get all decks list by filter and query',
        request=DeckListSerializer,
        responses={
            200: inline_serializer("SearchDecksAndFolders",
                                   {"decks": DeckDetailSerializer(many=True),
                                    "folders": FolderDetailSerializer(many=True)},
                                   many=False),
            (400, 'text/plain'): OpenApiResponse(description="Some fields is not exist"),
        }
    )
    def search(self, request):
        user = request.user
        filter = {}
        if request.data.get('filter'):
            filter = request.data['filter']
        query = ""
        if request.data.get('query'):
            query = request.data['query']

        decks = getDecks(filter)
        decks_data = []
        for deck in decks:
            if query in deck.deck_name:
                decks_data.append(getDeckData(deck, user))

        folders = Folder.objects.all()
        folders_data = []
        for folder in folders:
            if query in folder.folder_name:
                folders_data.append({"folder_name": folder.folder_name, "folder_id": folder.id})
        return Response({"decks": DeckDetailSerializer(decks_data, many=True).data, "folders": folders_data},
                        status=status.HTTP_200_OK)

    @extend_schema(
        description='Get deck by id',
        request=inline_serializer("GetDeckById", {"deck_id": fields.IntegerField()}, many=False),
        responses={
            200: DeckDetailSerializer
        }
    )
    def get_by_id(self, request):
        user = request.user
        if not request.data['deck_id']:
            raise ValidationError("field deck_id does not exist")
        deck_id = request.data['deck_id']
        deck_data = getDeckData(Deck.objects.get(id=deck_id), user)
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
        if not request.data['deck_name']:
            raise ValidationError("field deck_name does not exist")
        deck_name = request.data['deck_name']
        if not user.deck_set.filter(deck_name=deck_name):
            raise NotFound("User deck with this name does not found")
        deck = user.deck_set.get(deck_name=deck_name)
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
