from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.core.exceptions import ValidationError

from app_komunalka.models import MyUser


class UserCreateForm(UserCreationForm):
    # username = forms.CharField(label="login", widget=forms.TextInput())
    email = forms.EmailField(label="E-MAIL", widget=forms.EmailInput())
    password1 = forms.CharField(label="password", widget=forms.PasswordInput())
    password2 = forms.CharField(label="password confirmation", widget=forms.PasswordInput())

    class Meta:
        model = MyUser
        fields = ['email', 'password1', 'password2']

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if MyUser.objects.filter(email=email):
            raise ValidationError('This email is already registered')
        return email

    # def save(self, commit=True):
    #     user = super(UserCreateForm, self).save(commit=False)
    #     email = self.cleaned_data.get('email')
    #     username = email.partition('@')[0]
    #     if commit:
    #         user.username = username
    #         user.save()
    #     return user

    """НУЖНО проверить метод save(), чтобы сохранялся юзернейм от пароля до собачки в нём!!!!"""



