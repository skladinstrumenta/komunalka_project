from django.urls import path

from app_komunalka.views import HomePage

urlpatterns = [
    path('', HomePage.as_view(), name='home'),

    ]
