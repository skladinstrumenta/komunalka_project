from django.urls import path

from app_komunalka.views import *

urlpatterns = [
    path('', HomePage.as_view(), name='home'),
    path('index', IndexPage.as_view(), name='index'),
    path('register', RegistrationNewUserView.as_view(), name='register'),
    path('login', LoginUser.as_view(), name='login'),
    path('logout', LogoutUser.as_view(), name='logout'),
    path('kdlist', KomunalDataListView.as_view(), name='kd_list'),


    ]
