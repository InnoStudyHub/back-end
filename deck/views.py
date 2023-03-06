from drf_spectacular.utils import extend_schema, inline_serializer, OpenApiResponse, OpenApiParameter
from rest_framework import status, viewsets, fields
from rest_framework.exceptions import ValidationError, NotFound, PermissionDenied
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.utils import json
from rest_framework.views import APIView
from rest_framework_api_key.permissions import HasAPIKey

from analytic.helpers import add_event
from analytic.models import EventsCategoryModel
from deck.helpers.deck_helpers import logger, getDeckData
from deck.serializers.deck_serializer import DeckCreateSerializer, DeckRequestSerializer, \
    DeckDetailSerializer, DeckFromSheetSerializer
from deck.serializers.folder_serializers import FolderCreateSerializer, FolderDetailSerializer
from deck.models import Deck, Folder, Courses, Card


class DeckViewSet(viewsets.ViewSet):
    permission_classes = (IsAuthenticated, HasAPIKey)

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

        if not serializer.is_valid(raise_exception=True):
            logger.warning("Something wrong with request body")
            raise ValidationError(serializer.error_messages)

        serializer.save(author_id=user.id, files=request.data)
        response_data = getDeckData(serializer.instance, user)
        add_event(request.user, EventsCategoryModel.objects.get(event_category_name='Deck created'))
        return Response(response_data, status=status.HTTP_201_CREATED)

    @extend_schema(
        description='Create deck from sheet request',
        request=DeckFromSheetSerializer,
        responses={
            201: DeckDetailSerializer,
            (400, 'text/plain'): OpenApiResponse(description="Some fields is not exist"),
            (403, 'text/plain'): OpenApiResponse(description="Deck with this name exist")
        }
    )
    def create_from_google_sheet(self, request):
        user = request.user
        logger.info(f"Handle deck create from google sheet request: {request.data}, from user {user.id}")
        serializer = DeckFromSheetSerializer(data=request.data)

        if not serializer.is_valid(raise_exception=True):
            logger.warning("Something wrong with request body")
            raise ValidationError(serializer.error_messages)

        serializer.save(author_id=user.id)
        response_data = getDeckData(serializer.instance, user)
        add_event(request.user, EventsCategoryModel.objects.get(event_category_name='Deck created from google sheet'))
        return Response(response_data, status=status.HTTP_201_CREATED)

    @extend_schema(
        description='Get deck by id',
        request=inline_serializer("GetDeckById", {"deck_id": fields.IntegerField()}, many=False),
        responses={
            200: DeckDetailSerializer
        }
    )
    def get_by_id(self, request):
        user = request.user
        logger.info(f"Handle get deck by id: {request.data}, from user {user.id}")
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
        logger.info(f"Handle get deck by name: {request.data}, from user {user.id}")
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
        deck_data = getDeckData(deck, user)
        return Response(deck_data, status=status.HTTP_200_OK)


class FolderViewSet(viewsets.ViewSet):
    permission_classes = (IsAuthenticated, HasAPIKey)

    @extend_schema(
        request=FolderCreateSerializer,
        responses={
            201: FolderCreateSerializer,
            (400, 'text/plain'): OpenApiResponse(description="Some fields is not exist")
        }
    )
    def create(self, request, *args, **kwargs):
        logger.info(f"Handle create folder request: {request.data}")
        serializer = FolderCreateSerializer(data=request.data)

        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        folder = serializer.save()
        logger.info(f"Folder created: {folder}")
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @extend_schema(
        parameters=[
            OpenApiParameter("folderId", int)
        ],
        request=None,
        responses={
            200: DeckDetailSerializer(many=True)
        },
    )
    def get(self, request, *args, **kwargs):
        user = request.user
        logger.info(f"Handle get folder data: {request.data}")
        folder_id = request.GET.get('folderId', None)

        if not folder_id:
            raise ValidationError("folderId param does not exist")

        if not Folder.objects.filter(folder_id=folder_id).exists():
            raise NotFound("Folder not found")

        decks = Folder.objects.get(folder_id=folder_id).deck_set.all()
        decks_data = []
        for deck_opened in decks:
            deck = Deck.objects.get(deck_id=deck_opened.deck_id)
            decks_data.append(getDeckData(deck, user))
        return Response(DeckDetailSerializer(decks_data, many=True).data, status=status.HTTP_200_OK)

    @extend_schema(
        responses={
            200: FolderDetailSerializer(many=True)
        }
    )
    def list(self, request, *args, **kwargs):
        logger.info(f"Handle list all folders request: {request.data}")
        folders = Folder.objects.all()
        folders_data = []
        for folder in folders:
            folders_data.append({"folder_name": folder.folder_name, "folder_id": folder.folder_id})
        logger.info(f"Folders data: {folders_data}")
        return Response(folders_data, status=status.HTTP_200_OK)


class CoursesAPIView(APIView):
    permission_classes = [HasAPIKey]

    @extend_schema(
        request=inline_serializer("AddCourses",
                                  {"courses": inline_serializer(name="CourseData",
                                                                fields={"course_name": fields.CharField(),
                                                                        "course_year": fields.ChoiceField(
                                                                            choices=(1, 2, 3, 4))
                                                                        },
                                                                many=True)}),
        responses={
            (201, 'text/plain'): OpenApiResponse(description="Courses successfully added"),
            (400, 'text/plain'): OpenApiResponse(description="Some fields do not exist")
        },
    )
    def post(self, request):
        logger.info(f"Handle add courses request: {request.data}")
        courses_data = request.data.get('courses', [])
        for course_data in courses_data:
            course_name = course_data.get('course_name', '')
            course_year = course_data.get('course_year', None)

            if not course_name or not course_year:
                raise ValidationError('course_name or course_year field does not exist')

            course = Courses.objects.get_or_create(course_name=course_name, year=course_year)
            Folder.objects.get_or_create(folder_name=course[0].course_name)

        return Response(f"{len(courses_data)} courses successfully added", status=201)


class CardViewSet(viewsets.ViewSet):
    permission_classes = (IsAuthenticated, HasAPIKey)

    @extend_schema(
        description='Create deck request',
        request=inline_serializer(name="DeleteCardRequest",
                                  fields={"deck_id": fields.IntegerField(),
                                          "cards_id": fields.ListField(child=fields.IntegerField())
                                          }),
        responses={
            200: inline_serializer(name="DeleteCardResponse",
                                   fields={
                                        "errors": fields.ListField(child=fields.IntegerField())
                                   }),
            (400, 'text/plain'): OpenApiResponse(description="Some fields is not exist"),
            (404, 'text/plain'): OpenApiResponse(description="Deck is not found")
        }
    )
    def delete_cards(self, request):
        logger.info(f"Handle delete card request: {request.data}")
        user = request.user
        deck_id = request.data.get('deck_id', None)
        cards_id = request.data.get('cards_id', [])
        if deck_id is None:
            raise ValidationError('Parameter deck_id does not exist')

        deck = Deck.objects.filter(deck_id=deck_id).first()
        if deck is None:
            raise NotFound(f'Deck with deck_id={deck_id} does not exist')

        if deck.author is not user:
            raise PermissionDenied(f'User is not allowed to modify deck={deck_id}')

        cards = Card.objects.filter(card_id__in=cards_id, deck_id=deck_id)

        for card in cards:
            cards_id.remove(card.card_id)
            card.delete()

        data = {}
        if cards_id:
            logger.info(f"Error cards id: {cards_id}")
            data['errors'] = cards_id

        return Response(data, status=200)

    def copy_card(self, request):
        logger.info(f"Handle copy card request: {request.data}")
        source_card_id = request.data.get('source_card_id', None)
        destination_deck_id = request.data.get('destination_deck_id', None)
        

