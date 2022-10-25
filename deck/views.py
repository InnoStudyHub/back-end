from django import forms
from drf_spectacular.utils import extend_schema, inline_serializer, OpenApiResponse
from rest_framework import status, viewsets, fields
from rest_framework.exceptions import ValidationError
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.utils import json

from deck.serializers.deck_serializer import DeckCreateSerializer, DeckRequestSerializer, \
    DeckListSerializer, DeckDetailSerializer
from deck.serializers.folder_serializers import FolderCreateSerializer
from deck.models import Deck

def getDeckData(deck):
    cards = deck.card_set.all()
    data = deck.__dict__
    data['cards'] = []
    for card in cards:
        data['cards'].append(card.__dict__)
    serializer = DeckDetailSerializer(data=data)
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
        if request.data['data']:
            print(request.data['data'])
        else:
            print("Not exist")
        serializer = DeckCreateSerializer(data=json.loads(request.data['data']))
        if serializer.is_valid(raise_exception=True):
            serializer.save(author_id=user.id, files=request.data)
            response_data = getDeckData(serializer.instance)
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
                decks_data.append(getDeckData(deck))
        return Response(DeckDetailSerializer(decks_data, many=True).data, status=status.HTTP_200_OK)



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
