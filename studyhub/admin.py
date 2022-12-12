from django.contrib import admin

from deck.models import Deck, Card, Folder, Courses, UserFolderPermission
from user.models import User
from user_action.models import DeckOpened


@admin.register(Deck)
class DeckAdmin(admin.ModelAdmin):
    list_display = ("deck_id", "semester", "folder_name", "deck_name")

    def folder_name(self, deck):
        result = Folder.objects.get(folder_id=deck.folder_id)
        return result.folder_name


@admin.register(Card)
class CardAdmin(admin.ModelAdmin):
    list_display = ("card_id", "deck_name", "question_text", "question_image", "answer_text", "answer_images")

    def deck_name(self, card):
        result = Deck.objects.get(deck_id=card.deck_id)
        return result.deck_name


@admin.register(Folder)
class FolderAdmin(admin.ModelAdmin):
    pass


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    pass
