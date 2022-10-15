from django import forms
from rest_framework.exceptions import ValidationError

class CardCreateForm(forms.Form):
    question_text = forms.CharField(max_length=1024)
    question_image_key = forms.CharField(max_length=1024, required=False)
    answer_text = forms.CharField(max_length=1024)
    answer_image_keys = forms.BaseFormSet()

class DeckCreateForm(forms.Form):
    folder_id = forms.IntegerField()
    deck_name = forms.CharField(max_length=1024)
    course_year = forms.IntegerField()
    cards = forms.BaseFormSet()
