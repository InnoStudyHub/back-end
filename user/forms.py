from django.contrib.auth.forms import UserCreationForm
from django import forms
from rest_framework.exceptions import ValidationError
from rest_framework.validators import UniqueValidator

from user.models import User

class UploadFileForm(forms.Form):
    title = forms.CharField(max_length=255)

    def clean(self):
        cleaned_data = self.data
        for obj in cleaned_data:
            if obj == 'title':
                continue
            if cleaned_data[obj].content_type is None or cleaned_data[obj].content_type.split('/')[0] != 'image':
                raise ValidationError("Some file/files is not image")
