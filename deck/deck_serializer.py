from google.cloud import storage
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from rest_framework.fields import empty

from deck.card_serializers import CardCreateSerializer, CardResponseTemplateSerializer
from deck.models import Card, Deck, Folder
from user.models import User


def create_card(card, deck_id, files):
    card_serializer = CardCreateSerializer(data=card)
    if card_serializer.is_valid():
        card_serializer.save(deck_id=deck_id, files=files)
    else:
        raise ValidationError("Cards not valid")


class DeckCreateSerializer(serializers.Serializer):
    folder_id = serializers.IntegerField()
    deck_name = serializers.CharField(max_length=1024)
    course_year = serializers.IntegerField()
    cards = serializers.ListSerializer(child=CardCreateSerializer())

    class Meta:
        fields = ['deck_name', 'folder_id', 'course_year', 'cards']

    def validate_deck_name(self, value):
        data = self.get_initial()
        decks = Deck.objects.all().filter(folder_id=data['folder_id'], deck_name=value)
        if len(decks) != 0:
            raise ValidationError(f"Deck with this name with folder_id={data['folder_id']} exist")
        return value

    def create(self, validated_data):
        deck = Deck.objects.create(deck_name=validated_data['deck_name'], author_id=validated_data['author_id'],
                                   folder_id=validated_data['folder_id'], course_year=validated_data['course_year'])
        for card in validated_data['cards']:
            create_card(card=card, deck_id=deck.id, files=validated_data['files'])
        return deck


class DeckRequestTemplateSerializer(serializers.Serializer):
    data = DeckCreateSerializer()

    class Meta:
        fields = ['data']

class DeckResponseTemplateSerializer(serializers.Serializer):
    folder_id = serializers.IntegerField()
    author_id = serializers.IntegerField()
    deck_name = serializers.CharField(max_length=1024)
    course_year = serializers.IntegerField()
    cards = serializers.ListSerializer(child=CardResponseTemplateSerializer())

    class Meta:
        fields = ['deck_name', 'folder_id', 'author_id', 'course_year', 'cards']