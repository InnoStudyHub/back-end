from django import forms
from drf_spectacular.utils import extend_schema, inline_serializer, OpenApiResponse
from rest_framework import status, viewsets, fields
from rest_framework.exceptions import ValidationError, NotFound
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.utils import json

from deck.serializers.deck_serializer import DeckCreateSerializer, DeckRequestSerializer, \
    DeckListSerializer, DeckDetailSerializer, DeckPreviewSerializer
from deck.serializers.folder_serializers import FolderCreateSerializer
from deck.models import Deck
from user.models import User


def getDeckData(deck, user):
    cards = deck.card_set.all()
    data = deck.__dict__
    data['cards'] = []
    data['is_favourite'] = user.favourite_decks.contains(deck)
    for card in cards:
        data['cards'].append(card.__dict__)
    serializer = DeckDetailSerializer(data=data)
    if not serializer.is_valid(raise_exception=True):
        raise ValidationError(serializer.error_messages)
    return serializer.data

def getDeckPreview(deck, user):
    cards = deck.card_set.all()
    data = deck.__dict__
    data['cards'] = len(cards)
    data['is_favourite'] = user.favourite_decks.contains(deck)
    serializer = DeckPreviewSerializer(data=data)
    if not serializer.is_valid(raise_exception=True):
        raise ValidationError(serializer.error_messages)
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
        data = json.loads(request.data['data'])
        serializer = DeckCreateSerializer(data=data)
        if serializer.is_valid(raise_exception=True):
            serializer.save(author_id=user.id, files=request.data)
            response_data = getDeckData(serializer.instance, user)
            return Response(response_data, status=status.HTTP_201_CREATED)
        else:
            raise ValidationError(serializer.error_messages)

    @extend_schema(
        description='Get all decks list by filter and query',
        request=DeckListSerializer,
        responses={
            200: DeckDetailSerializer(many=True),
            (400, 'text/plain'): OpenApiResponse(description="Some fields is not exist"),
        }
    )
    def list(self, request):
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
        return Response(DeckDetailSerializer(decks_data, many=True).data, status=status.HTTP_200_OK)

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


class FolderCreateView(CreateAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = FolderCreateSerializer

    @extend_schema(
        responses={
            201: FolderCreateSerializer,
            (400, 'text/plain'): OpenApiResponse(description="Some fields is not exist")
        }
    )
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
