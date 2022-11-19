from rest_framework import serializers
from rest_framework.exceptions import ValidationError, NotFound

from deck.helpers.card_helpers import parseGoogleSheet, getCardDataAndFiles
from deck.serializers.card_serializers import CardCreateSerializer, CardDetailSerializer
from deck.models import Deck, Folder
from user.models import User


class DeckCreateSerializer(serializers.Serializer):
    folder_id = serializers.IntegerField()
    deck_name = serializers.CharField(max_length=1024)
    semester = serializers.CharField(max_length=255)
    cards = serializers.ListSerializer(child=CardCreateSerializer(), allow_empty=True, required=False)

    class Meta:
        fields = ['deck_name', 'folder_id', 'semester', 'cards']

    def validate_folder_id(self, value):
        if not Folder.objects.filter(folder_id=value):
            raise NotFound(f"Folder does not exist")
        return value

    def create_card(self, card, deck_id, files):
        card_serializer = CardCreateSerializer(data=card)
        if card_serializer.is_valid(raise_exception=True):
            card_serializer.save(deck_id=deck_id, files=files)
        else:
            raise ValidationError("Cards not valid")

    def create(self, validated_data):
        user = User.objects.get(id=validated_data['author_id'])

        if user.deck_set.all().filter(deck_name=validated_data['deck_name'], folder_id=validated_data['folder_id']):
            raise ValidationError(f"Deck with name {validated_data['deck_name']} already exist for this user")

        deck = Deck.objects.create(deck_name=validated_data['deck_name'], author_id=user.id,
                                   folder_id=validated_data['folder_id'], semester=validated_data['semester'])

        if not validated_data.get('cards'):
            validated_data['cards'] = []

        try:
            for card in validated_data['cards']:
                self.create_card(card=card, deck_id=deck.deck_id, files=validated_data['files'])
        except Exception as e:
            deck.delete()
            raise e

        return deck


class DeckFromSheetSerializer(DeckCreateSerializer):
    url = serializers.CharField(max_length=1024)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields.pop('cards')

    class Meta:
        fields = ['folder_id', 'deck_name', 'semester', 'url']

    def create(self, validated_data):
        user = User.objects.get(id=validated_data['author_id'])

        if user.deck_set.all().filter(deck_name=validated_data['deck_name'], folder_id=validated_data['folder_id']):
            raise ValidationError(f"Deck with name {validated_data['deck_name']} already exist for this user")

        deck = Deck.objects.create(deck_name=validated_data['deck_name'], author_id=user.id,
                                   folder_id=validated_data['folder_id'], semester=validated_data['semester'])

        try:
            cards = parseGoogleSheet(validated_data['url'])
            for card in cards:
                card_count = len(deck.card_set.all())
                data_and_files = getCardDataAndFiles(card, card_count)
                self.create_card(card=data_and_files['card_data'],
                                 deck_id=deck.deck_id,
                                 files=data_and_files['files'])
        except Exception as e:
            deck.delete()
            raise e

        return deck


class DeckRequestSerializer(serializers.Serializer):
    data = DeckCreateSerializer()

    class Meta:
        fields = ['data']


class DeckDetailSerializer(serializers.Serializer):
    deck_id = serializers.IntegerField()
    folder_id = serializers.IntegerField()
    author_id = serializers.IntegerField()
    deck_name = serializers.CharField(max_length=1024)
    semester = serializers.CharField(max_length=255)
    cards = serializers.ListSerializer(child=CardDetailSerializer())
    is_favourite = serializers.BooleanField()

    class Meta:
        fields = ['deck_name', 'folder_id', 'author_id', 'semester', 'cards', 'deck_id', 'is_favourite']


class DeckPreviewSerializer(serializers.Serializer):
    deck_id = serializers.IntegerField()
    folder_id = serializers.IntegerField()
    author_id = serializers.IntegerField()
    deck_name = serializers.CharField(max_length=1024)
    semester = serializers.CharField(max_length=255)
    cards = serializers.IntegerField()
    is_favourite = serializers.BooleanField()

    class Meta:
        fields = ['deck_name', 'folder_id', 'author_id', 'semester', 'cards', 'deck_id', 'is_favourite']


class FilterRequestSerializer(serializers.Serializer):
    semester = serializers.CharField(max_length=1024, allow_blank=True, allow_null=True)
    folder_id = serializers.IntegerField(allow_null=True)

    class Meta:
        fields = ['query', 'semester']


class DeckListSerializer(serializers.Serializer):
    filter = FilterRequestSerializer()
    query = serializers.CharField(max_length=1024, allow_blank=True, allow_null=True)

    class Meta:
        fields = ['filter', 'query']
