from django.contrib.auth.models import AbstractUser
from django.db import models


class MyUser(AbstractUser):
    email = models.EmailField(max_length=100, unique=True)
    adress = models.ManyToManyField('Adress', related_name="adress_of_user", verbose_name="Адрес")

    class Meta:
        ordering = ['username']
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"

    def __str__(self):
        return self.username


class Adress(models.Model):
    country = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    street = models.CharField(max_length=255)
    house = models.CharField(max_length=10)
    corps = models.CharField(max_length=3, blank=True, null=True)
    room = models.CharField(max_length=10, blank=True, null=True)
    user = models.ManyToManyField(MyUser, related_name='users_adress', blank=True, null=True)

    class Meta:
        ordering = ['country', 'city', 'street', 'house', 'corps', 'room']
        verbose_name = "Адрес"
        verbose_name_plural = "Адреса"

    def __str__(self):
        if self.corps and self.room:
            return f"{self.country}, {self.city}, {self.street}, {self.house}-{self.corps}, кв.{self.room}"
        elif self.corps:
            return f"{self.country}, {self.city}, {self.street}, {self.house}-{self.corps}"
        elif self.room:
            return f"{self.country}, {self.city}, {self.street}, {self.house}, кв.{self.room}"
        else:
            return f"{self.country}, {self.city}, {self.street}, {self.house}"


# class KomunalData(models.Model):
#     gas = models.PositiveIntegerField(float=True)
#     water = models.PositiveIntegerField(float=True)
#     light = models.PositiveIntegerField(float=True)
#     user = models.ForeignKey(MyUser, related_name='users_komdata', verbose_name='Пользователь',
#                              on_delete=models.CASCADE)
#     date_create = models.DateTimeField(auto_now_add=True)
#     date_create = models.DateTimeField(auto_now_add=True)



