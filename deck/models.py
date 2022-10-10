from django.db import models

from user.models import User

class Folder(models.Model):
    folder_name = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Deck(models.Model):
    deck_name = models.CharField(max_length=255)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    folder = models.ForeignKey(Folder, on_delete=models.CASCADE, blank=True)
    course_year = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Card(models.Model):
    question_description = models.CharField(max_length=1024, blank=False, null=True)
    question_image = models.CharField(max_length=1024, blank=False, null=True)
    answer_description = models.CharField(max_length=1024, blank=False, null=True)
    question_images = models.JSONField(blank=False, null=True)
    deck = models.ForeignKey(Deck, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
