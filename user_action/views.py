from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import extend_schema, inline_serializer, OpenApiExample, OpenApiResponse
from rest_framework import fields, status, viewsets
from rest_framework.exceptions import PermissionDenied, ValidationError
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from deck.models import Deck
from user.models import User


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
        request=inline_serializer("FavouritesAdd", {"deck_id": fields.IntegerField()}, many=False),
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
