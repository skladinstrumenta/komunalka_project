from datetime import datetime

from django.contrib.auth import authenticate
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django import forms
from django.core.exceptions import ValidationError

from app_komunalka.models import MyUser, KomunalData, Adress

years_list = list(range(datetime.now().year - 100, datetime.now().year + 1, -1))
now = datetime.now()


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
        if MyUser.objects.filter(email=email).exists():
            raise ValidationError('This email is already registered')
        return email

    def save(self, commit=True):
        user = super(UserCreateForm, self).save(commit=False)
        email = self.cleaned_data.get('email')
        username = email.partition('@')[0]
        if commit:
            user.username = username
            user.save()
        return user


# class LoginForm(forms.ModelForm):
#     # username = forms.CharField(label='login', widget=forms.HiddenInput(), required=False)
#     email = forms.EmailField(label="E-MAIL", widget=forms.EmailInput())
#     password = forms.CharField(label="password", widget=forms.PasswordInput())
#     class Meta:
#         model = MyUser
#         fields = ['email', 'password']
#
#     def clean(self):
#         return self.cleaned_data

class LoginForm(AuthenticationForm):
    email = forms.EmailField(label="E-mail", widget=forms.EmailInput())
    username = forms.CharField(label='login', widget=forms.HiddenInput(), required=False)
    password = forms.CharField(label="Password", widget=forms.PasswordInput())

    def clean(self):
        email = self.cleaned_data.get('email')
        valid_email = MyUser.objects.filter(email=email).exists()
        if valid_email:
            username = MyUser.objects.get(email=email).username
            password = self.cleaned_data.get('password')
            if username is not None and password:
                self.user_cache = authenticate(
                    self.request, username=username, password=password
                )
                if self.user_cache is None:
                    raise self.get_invalid_login_error()
                else:
                    self.confirm_login_allowed(self.user_cache)

        else:
            raise ValidationError('msg')
            return self.cleaned_data
        return self.cleaned_data

    # def clean_email(self):
    #     email = self.cleaned_data.get('email')
    #     if not MyUser.objects.filter(email=email).exists():
    #         raise ValidationError('This email is not registered')
    #     return email
    #
    # def clean_username(self):
    #     email = self.clean_email()
    #     user_instance = MyUser.objects.get(email=email)
    #     username = user_instance.username
    #     # password = user_instance.password
    #     # self.user_cache = authenticate(self.request, username=username, password=password)
    #     if not username:
    #         raise ValidationError('This email is not registered')
    #     return username


class DataCreateForm(forms.ModelForm):
    komunaldata_dateon = forms.DateField(label='Дата начисления',
                                         initial=datetime.today(),
                                         widget=forms.SelectDateWidget(years=years_list))
    # komunaldata_dateoff = forms.DateField(label='Дата завершения начисления',
    #                                       widget=forms.SelectDateWidget(years=years_list))

    # def __init__(self, *args, **kwargs):
    #     user = kwargs.pop('user', None)
    #     super(DataCreateForm, self).__init__(*args, **kwargs)
    #     if user and user.is_authenticated:
    #         self.fields['adress'].queryset = Adress.objects.filter(user__username='skladinstrumenta23')


    class Meta:
        model = KomunalData
        fields = ['gas', 'water', 'light', 'adress', 'komunaldata_dateon']
        # fields = ['gas', 'water', 'light', 'adress']

        # def clean_gas(self):
        #     gas = self.cleaned_data.get('gas')
        #     if not gas % 2:
        #         raise ValidationError('fuck')
        #     return gas

    def clean(self):
        gas = self.cleaned_data.get('gas')
        water = self.cleaned_data.get('water')
        if gas < 0:
            raise ValidationError('fuck gas')
        # elif not water % 2:
        #     raise ValidationError('fuck water')
        # return gas


class DataUpdateForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        user_id = user.id
        super(DataUpdateForm, self).__init__(*args, **kwargs)
        if user and user.is_authenticated and not user.is_superuser:
            self.fields['adress'].queryset = Adress.objects.filter(user__id=user_id)

    class Meta:
        model = KomunalData
        fields = ['gas', 'water', 'light', 'adress', 'komunaldata_dateon']
        # fields = '__all__'

class NewAdressForm(forms.ModelForm):

    class Meta:
        model = Adress
        fields = '__all__'
        # exclude = 'user'



