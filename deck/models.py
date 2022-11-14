from django.db import models

from user.models import User

class Folder(models.Model):
    folder_id = models.AutoField(primary_key=True)
    folder_name = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'folder'

class Deck(models.Model):
    deck_id = models.AutoField(primary_key=True)
    deck_name = models.CharField(max_length=255)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    folder = models.ForeignKey(Folder, on_delete=models.CASCADE, blank=True)
    semester = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'deck'

class Card(models.Model):
    card_id = models.AutoField(primary_key=True)
    question_text = models.CharField(max_length=1024, blank=True, null=True)
    question_image = models.CharField(max_length=1024, blank=True, null=True)
    answer_text = models.CharField(max_length=1024, blank=True, null=True)
    answer_images = models.JSONField(null=True)
    deck = models.ForeignKey(Deck, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'card'

