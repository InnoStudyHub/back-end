from django.contrib import admin

from deck.models import Deck, Card, Folder, Courses, UserFolderPermission
from user.models import User


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
    list_display = ("folder_id", "folder_name")
    pass


@admin.register(Courses)
class CoursesAdmin(admin.ModelAdmin):
    list_display = ("id", "course_name", "year")
    pass


@admin.register(UserFolderPermission)
class UserFolderPermissionAdmin(admin.ModelAdmin):
    list_display = ("user_email", "folder_name", "access_type")

    def user_email(self, user_folder_permission):
        return user_folder_permission.user.email

    def folder_name(self, user_folder_permission):
        return user_folder_permission.folder.folder_name
    pass


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ("id", "email", "fullname", "is_admin")
    pass
