# Generated by Django 4.1.6 on 2023-04-09 18:55

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_komunalka', '0005_alter_komunaldata_komunaldata_dateon'),
    ]

    operations = [
        migrations.AlterField(
            model_name='komunaldata',
            name='komunaldata_dateon',
            field=models.DateField(blank=True, default=datetime.date(2023, 4, 9), null=True, verbose_name='Данные за месяц'),
        ),
    ]