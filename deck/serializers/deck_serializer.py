from rest_framework import serializers
from rest_framework.exceptions import ValidationError, PermissionDenied

from deck.serializers.card_serializers import CardCreateSerializer, CardDetailSerializer
from deck.models import Deck, Folder


class DeckCreateSerializer(serializers.Serializer):
    folder_id = serializers.IntegerField()
    deck_name = serializers.CharField(max_length=1024)
    semester = serializers.CharField(max_length=255)
    cards = serializers.ListSerializer(child=CardCreateSerializer())

    class Meta:
        fields = ['deck_name', 'folder_id', 'semester', 'cards']

    def create_card(self, card, deck_id, files):
        card_serializer = CardCreateSerializer(data=card)
        if card_serializer.is_valid(raise_exception=True):
            card_serializer.save(deck_id=deck_id, files=files)
        else:
            raise ValidationError("Cards not valid")

    def validate_folder_id(self, value):
        if Folder.objects.get(id=value) is None:
            raise PermissionDenied(f"Folder does not exist")
        return value

    def validate_deck_name(self, value):
        data = self.get_initial()
        decks = Deck.objects.all().filter(folder_id=data['folder_id'], deck_name=value)
        if len(decks) != 0:
            raise PermissionDenied(f"Deck with this name exist")
        return value

    def create(self, validated_data):
        deck = Deck.objects.create(deck_name=validated_data['deck_name'], author_id=validated_data['author_id'],
                                   folder_id=validated_data['folder_id'], semester=validated_data['semester'])
        for card in validated_data['cards']:
            self.create_card(card=card, deck_id=deck.id, files=validated_data['files'])
        return deck


class DeckRequestSerializer(serializers.Serializer):
    data = DeckCreateSerializer()

    class Meta:
        fields = ['data']


class DeckDetailSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    folder_id = serializers.IntegerField()
    author_id = serializers.IntegerField()
    deck_name = serializers.CharField(max_length=1024)
    semester = serializers.CharField(max_length=255)
    cards = serializers.ListSerializer(child=CardDetailSerializer())

    class Meta:
        fields = ['deck_name', 'folder_id', 'author_id', 'semester', 'cards', 'id']


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

