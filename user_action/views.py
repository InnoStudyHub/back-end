from drf_spectacular.utils import extend_schema, inline_serializer, OpenApiResponse, OpenApiParameter
from rest_framework import fields, status, viewsets
from rest_framework.exceptions import PermissionDenied, ValidationError, NotFound
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_api_key.permissions import HasAPIKey

from deck.helpers.deck_helpers import getDecks, logger
from deck.models import Deck, Folder, UserFolderPermission
from deck.serializers.deck_serializer import DeckDetailSerializer, DeckListSerializer
from deck.serializers.folder_serializers import FolderDetailSerializer
from deck.views import getDeckData
from user.models import User
from user_action.models import DeckOpened


class FavouritesView(viewsets.ViewSet):
    permission_classes = (IsAuthenticated, HasAPIKey)

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
        logger.info(f"Handle remove deck from favourite request: {request.data}, from user {user.id}")
        if not request.data.get('deck_id'):
            raise ValidationError(detail={'deck_id': 'field is not exist'}, code=400)
        deck_id = request.data['deck_id']

        if user.favourite_decks.filter(deck_id=deck_id):
            raise PermissionDenied("This deck is already favourite by user")

        user.favourite_decks.add(Deck.objects.get(deck_id=deck_id))
        logger.info(f"Deck add to favorites, deck_id: {deck_id}")
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
        logger.info(f"Handle remove deck from favourite request: {request.data}, from user {user.id}")
        if not request.data.get('deck_id'):
            raise ValidationError(detail={'deck_id': 'field is not exist'}, code=400)
        deck_id = request.data['deck_id']

        if not user.favourite_decks.filter(deck_id=deck_id):
            raise PermissionDenied("This deck is not favourite by user")

        user.favourite_decks.remove(Deck.objects.get(deck_id=deck_id))
        logger.info(f"Deck removed from favorites, deck_id: {deck_id}")
        return Response("Deck successfully remove from favourites", status=status.HTTP_201_CREATED)

    @extend_schema(
        request=None,
        responses={
            (200, 'application/json'): DeckDetailSerializer(many=True)
        }
    )
    def get_favourites(self, request, *args, **kwargs):
        user = request.user
        logger.info(f"Handle get user favourites request: {request.data}, from user {user.id}")
        decks = user.favourite_decks.all()
        decks_data = []
        for deck in decks:
            decks_data.append(getDeckData(deck, user))
        logger.info(f"Decks data: {decks_data}")

        return Response(DeckDetailSerializer(decks_data, many=True).data, status=status.HTTP_200_OK)


class UserDeckView(viewsets.ViewSet):
    permission_classes = (IsAuthenticated, HasAPIKey)

    @extend_schema(
        request=None,
        responses={
            (200, 'application/json'): DeckDetailSerializer(many=True)
        }
    )
    def get_user_decks(self, request, *args, **kwargs):
        user = request.user
        logger.info(f"Handle user deck request: {request.data}, from user {user.id}")
        decks = user.deck_set.all()
        decks_data = []
        for deck in decks:
            decks_data.append(getDeckData(deck, user))
        logger.info(f"Decks data: {decks_data}")

        return Response(DeckDetailSerializer(decks_data, many=True).data, status=status.HTTP_200_OK)

    @extend_schema(
        request=None,
        responses={
            (200, 'application/json'): DeckDetailSerializer(many=True)
        }
    )
    def get_recent_decks(self, request, *args, **kwargs):
        user = request.user
        logger.info(f"Handle user recent deck request: {request.data}, from user {user.id}")
        decks = user.deckopened_set.order_by('view_at').reverse()[:15]
        decks_data = []
        for deck_opened in decks:
            deck = Deck.objects.get(deck_id=deck_opened.deck_id)
            decks_data.append(getDeckData(deck, user))
        logger.info(f"Recent deck datas: {decks_data}")
        return Response(DeckDetailSerializer(decks_data, many=True).data, status=status.HTTP_200_OK)

    @extend_schema(
        request=None,
        responses={
            (200, 'application/json'): FolderDetailSerializer(many=True)
        }
    )
    def get_for_you_decks(self, request, *args, **kwargs):
        user = request.user
        logger.info(f"Handle user for you deck request: {request.data}, from user {user.id}")
        user_folder_permission = UserFolderPermission.objects.filter(user=user)
        folders = []

        if user_folder_permission.exists():
            for permission in user_folder_permission:
                folders.append(permission.folder)
        else:
            folders = Folder.objects.all()

        folders_data = []
        for folder in folders:
            folders_data.append({"folder_name": folder.folder_name, "folder_id": folder.folder_id})
        logger.info(f"Folders data: {folders_data}")
        return Response(folders_data, status=status.HTTP_200_OK)


class SearchView(APIView):
    permission_classes = (IsAuthenticated, HasAPIKey)

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
        logger.info(f"Handle search request: {request.data}, from user {user.id}")
        filter = {}
        if request.data.get('filter'):
            filter = request.data['filter']
        query = ""
        if request.data.get('query'):
            query = request.data['query']
        logger.info(f"Filter: {filter}, query {query}")

        decks = getDecks(filter)
        decks_data = []
        for deck in decks:
            if query.lower() in deck.deck_name.lower():
                decks_data.append(getDeckData(deck, user))
        logger.info(f"Find decks data: {decks_data}")

        folders = Folder.objects.all()
        folders_data = []
        for folder in folders:
            if query.lower() in folder.folder_name.lower():
                folders_data.append({"folder_name": folder.folder_name, "folder_id": folder.folder_id})
        logger.info(f"Find folders data: {folders_data}")

        return Response({"decks": DeckDetailSerializer(decks_data, many=True).data, "folders": folders_data},
                        status=status.HTTP_200_OK)


class UserInfoAPIView(APIView):
    permission_classes = [HasAPIKey]

    @extend_schema(
        parameters=[
            OpenApiParameter("userId", int)
        ],
        request=None,
        responses={
            200: inline_serializer(name='GetUserInfoById',
                                   fields={"email": fields.CharField(),
                                           "fullname": fields.CharField()})
        },
    )
    def get(self, request, *args, **kwargs):
        user_id = request.GET.get('userId', None)
        if not user_id:
            raise ValidationError('userId param does not exist')
        if User.objects.filter(id=user_id).exists():
            user = User.objects.get(id=user_id)
            user_response = {
                "email": user.email,
                "fullname": user.fullname
            }
            return Response(user_response, status=200)

        return Response("User does not exist", status=404)


class UserLogsView(viewsets.ViewSet):
    permission_classes = (IsAuthenticated, HasAPIKey)

    @extend_schema(
        description='Handle deck viewed by user',
        request=inline_serializer("UserLogDeck",
                                  {"deck_id": fields.IntegerField()},
                                  many=False),
        responses={
            200: None,
            (400, 'text/plain'): OpenApiResponse(description="Some fields is not exist"),
            (404, 'text/plain'): OpenApiResponse(description="Deck is not exist"),
        }
    )
    def deck_opened(self, request):
        user = request.user
        logger.info(f"Handle deck opened request: {request.data}, from user {user.id}")
        if not request.data.get('deck_id'):
            raise ValidationError('Field deck_id does not exist')
        deck_id = request.data['deck_id']

        if not Deck.objects.filter(deck_id=deck_id):
            raise NotFound(f'Deck with deck_id={deck_id} not found')

        deck_opened = DeckOpened.objects.get_or_create(deck_id=deck_id, user_id=user.id)
        deck_opened[0].save()
        logger.info(f"Saved opened deck log, deck_view_id - {deck_opened[0].deck_view_id}")
        return Response(status=status.HTTP_200_OK)

