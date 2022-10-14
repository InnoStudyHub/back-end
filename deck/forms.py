from django import forms
from rest_framework.exceptions import ValidationError

def validateImage(image):
    return (image.content_type is not None and image.content_type.split('/')[0] == 'image')


class UploadFileForm(forms.Form):
    title = forms.CharField(max_length=255)
    def clean(self):
        files = self.files
        print(files)
        for file in files:
            if not validateImage(files[file]):
                raise ValidationError("Some file/files is not image")

class CardForm(forms.Form):
    question_description = forms.CharField(max_length=1024)
    question_image = forms.CharField(max_length=1024)
    answer_description = forms.CharField(max_length=1024)
    question_images = forms.JSONField()
