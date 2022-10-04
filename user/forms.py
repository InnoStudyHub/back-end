from django.contrib.auth.forms import UserCreationForm
from django import forms
from user.models import User

class RegisterForm(UserCreationForm):
    password = forms.CharField(label='password', widget=forms.PasswordInput)

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('email', 'fullname')

    def clean_email(self):
        email = self.cleaned_data.get('email')
        qs = User.objects.filter(email=email)
        if qs.exists():
            raise forms.ValidationError(f"User with {email} already exists")
        return

    def save(self, commit=True):
        user = User.objects.create_user(
            self.cleaned_data['email'],
            self.cleaned_data['fullname'],
            self.cleaned_data['password']
        )
        return user
