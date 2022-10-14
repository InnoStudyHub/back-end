from django.contrib.auth.forms import UserCreationForm
from django import forms
from rest_framework.exceptions import ValidationError
from rest_framework.validators import UniqueValidator

from user.models import User

def isImage(image):
    return (image.content_type is not None and image.content_type.split('/')[0] == 'image')


class ImageForm(forms.Form):
    image = None
    def clean(self):
        files = self.files
        if len(files) > 1:
            raise ValidationError("Not correct ImageForm")
        key = list(files)[0]
        if not isImage(files[key]):
            raise ValidationError(f"{key} file is not image")
        self.image = files[key]

class CardForm(forms.Form):
    question_description = forms.CharField(max_length=1024)
    question_image = None
    answer_description = forms.CharField(max_length=1024)
    answer_images = []

    def clean(self):
        files = self.files
        if files.get('question_image') is not None:
            self.question_image = ImageForm(files={'question_image': files.get('question_image')})
        for i in range(len(files)):
            if files.get(f'answer_image_{i}') is None:
                break
            self.answer_images.append(ImageForm(files={f'answer_image_{i}': files.get(f'answer_image_{i}')}))


class UploadFileForm(forms.Form):
    title = forms.CharField(max_length=255)
    def clean(self):
        files = self.files
        print(files)
        for file in files:
            if not validateImage(files[file]):
                raise ValidationError("Some file/files is not image")

