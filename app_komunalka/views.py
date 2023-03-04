from django.contrib.auth import authenticate, login
from django.shortcuts import render
from django.views.generic import TemplateView, CreateView

from app_komunalka.forms import UserCreateForm
from app_komunalka.models import MyUser


class HomePage(TemplateView):
    template_name = 'home.html'


class RegistrationNewUserView(CreateView):
    template_name = "registration.html"
    form_class = UserCreateForm
    success_url = '/'

    def form_valid(self, form):
        valid = super().form_valid(form)
        email = form.cleaned_data.get('email')
        password = form.cleaned_data.get('password1')
        print(MyUser.objects.last())
        user = authenticate(email=email, password=password)
        login(self.request, user)
        return valid



class LoginUser(CreateView):
    pass


class CreateNewKomubalDataView(CreateView):
    pass