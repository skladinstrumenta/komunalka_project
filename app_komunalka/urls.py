from django.urls import path

from app_komunalka.views import *

urlpatterns = [
    path('', HomePage.as_view(), name='home'),
    path('register', RegistrationNewUserView.as_view(), name='register'),

    ]
