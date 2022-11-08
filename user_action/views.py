from drf_spectacular.utils import extend_schema, inline_serializer, OpenApiResponse
from rest_framework import fields, status, viewsets
from rest_framework.exceptions import PermissionDenied, ValidationError
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from deck.models import Deck
from deck.serializers.deck_serializer import DeckDetailSerializer
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

        if user.favourite_decks.filter(id=deck_id):
            raise PermissionDenied("This deck is already favourite by user")

        user.favourite_decks.add(Deck.objects.get(id=deck_id))
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

        if not user.favourite_decks.filter(id=deck_id):
            raise PermissionDenied("This deck is not favourite by user")

        user.favourite_decks.remove(Deck.objects.get(id=deck_id))
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
