from drf_spectacular.utils import extend_schema, inline_serializer, OpenApiResponse
from rest_framework import fields, status, viewsets
from rest_framework.exceptions import PermissionDenied, ValidationError
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from deck.helpers.deck_helpers import getDecks
from deck.models import Deck, Folder
from deck.serializers.deck_serializer import DeckDetailSerializer, DeckListSerializer
from deck.serializers.folder_serializers import FolderDetailSerializer
from deck.views import getDeckData


class FavouritesView(viewsets.ViewSet):
    permission_classes = (IsAuthenticated,)

    @extend_schema(
        request=inline_serializer("FavouritesAdd", {"deck_id": fields.IntegerField()}, many=False),
        responses={
            (200, 'text/plain'): OpenApiResponse(description="Deck successfully add to favourites"),
            (400, 'text/plain'): OpenApiResponse(description="Some fields is not exist"),
            (403, 'text/plain'): OpenApiResponse(description="Deck is already favourite by user")
        }
    )
    def add_favourite(self, request, *args, **kwargs):
        user = request.user
        if not request.data.get('deck_id'):
            raise ValidationError(detail={'deck_id': 'field is not exist'}, code=400)
        deck_id = request.data['deck_id']

        if user.favourite_decks.filter(deck_id=deck_id):
            raise PermissionDenied("This deck is already favourite by user")

        user.favourite_decks.add(Deck.objects.get(deck_id=deck_id))
        return Response("Deck successfully add to favourites", status=status.HTTP_201_CREATED)

    @extend_schema(
        request=inline_serializer("FavouritesRemove", {"deck_id": fields.IntegerField()}, many=False),
        responses={
            (200, 'text/plain'): OpenApiResponse(description="Deck successfully remove from favourites"),
            (400, 'text/plain'): OpenApiResponse(description="Some fields is not exist"),
            (403, 'text/plain'): OpenApiResponse(description="Deck is not favourite by user")
        }
    )
    def remove_favourite(self, request, *args, **kwargs):
        user = request.user
        if not request.data.get('deck_id'):
            raise ValidationError(detail={'deck_id': 'field is not exist'}, code=400)
        deck_id = request.data['deck_id']

        if not user.favourite_decks.filter(deck_id=deck_id):
            raise PermissionDenied("This deck is not favourite by user")

        user.favourite_decks.remove(Deck.objects.get(deck_id=deck_id))
        return Response("Deck successfully remove from favourites", status=status.HTTP_201_CREATED)

    @extend_schema(
        request=None,
        responses={
            (200, 'application/json'): DeckDetailSerializer(many=True)
        }
    )
    def get_favourites(self, request, *args, **kwargs):
        user = request.user
        decks = user.favourite_decks.all()
        decks_data = []
        for deck in decks:
            decks_data.append(getDeckData(deck, user))
        return Response(DeckDetailSerializer(decks_data, many=True).data, status=status.HTTP_200_OK)


class UserDeckView(viewsets.ViewSet):
    permission_classes = (IsAuthenticated,)

    @extend_schema(
        request=None,
        responses={
            (200, 'application/json'): DeckDetailSerializer(many=True)
        }
    )
    def get_user_decks(self, request, *args, **kwargs):
        user = request.user
        decks = user.deck_set.all()
        decks_data = []
        for deck in decks:
            decks_data.append(getDeckData(deck, user))
        return Response(DeckDetailSerializer(decks_data, many=True).data, status=status.HTTP_200_OK)


class SearchView(APIView):
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
    def post(self, request):
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
                folders_data.append({"folder_name": folder.folder_name, "folder_id": folder.folder_id})
        return Response({"decks": DeckDetailSerializer(decks_data, many=True).data, "folders": folders_data},
                        status=status.HTTP_200_OK)
