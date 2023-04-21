import datetime

from django.contrib.auth.models import AbstractUser
from django.core.validators import MinValueValidator
from django.db import models
from django.db.models.expressions import d


class MyUser(AbstractUser):
    username = models.CharField(max_length=100, blank=True, null=True, unique=True)
    email = models.EmailField(max_length=100, unique=True)
    # adress = models.ManyToManyField('Adress', related_name="adress_of_user", verbose_name="Адрес")

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
    user = models.ManyToManyField(MyUser, related_name='users_adress')
    tarif_gas = models.FloatField(validators=[MinValueValidator(0)], default=1)
    tarif_delivery_gas = models.FloatField(validators=[MinValueValidator(0)], default=1)
    tarif_water = models.FloatField(validators=[MinValueValidator(0)], default=1)
    tarif_light = models.FloatField(validators=[MinValueValidator(0)], default=1)
    tarif_musor = models.FloatField(validators=[MinValueValidator(0)], default=1)
    tarif_obsg = models.FloatField(validators=[MinValueValidator(0)], default=1)
    debt = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    date_create_adress = models.DateTimeField(auto_now_add=True)
    date_update_adress = models.DateTimeField(auto_now=True)

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


class KomunalData(models.Model):
    gas = models.PositiveIntegerField()
    water = models.PositiveIntegerField()
    light = models.PositiveIntegerField()
    adress = models.ForeignKey(Adress, related_name='adress_komunaldata', verbose_name='Адрес',
                               on_delete=models.CASCADE)
    komunaldata_dateon = models.DateField(verbose_name="Данные за месяц", blank=True, null=True,
                                          default=datetime.date.today())
    # komunaldata_dateoff = models.DateField(verbose_name="Дата завершения начисления")

    date_create = models.DateTimeField(auto_now_add=True)
    date_update = models.DateTimeField(auto_now=True)
    result = models.FloatField(blank=True, null=True, verbose_name="Итого, грн")

    class Meta:
        ordering = ['-date_update', '-date_create']
        verbose_name_plural = "Показания счётчиков"

    def __str__(self):
        return f'{self.date_create.strftime("%d.%m.%y %H:%M")} - ' \
               f'{self.adress.city}/{self.adress.street}/{self.adress.house}' \
               f'-{self.adress.corps if self.adress.corps else ""}' \
               f'/кв{self.adress.room if self.adress.room else ""} '


class Repayment(models.Model):
    adress = models.ForeignKey(Adress, verbose_name='Aдрес', on_delete=models.CASCADE)
    summ_of_repayment = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    date_of_repayment = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-date_of_repayment']
        verbose_name_plural = "Погашения задолженностей"
