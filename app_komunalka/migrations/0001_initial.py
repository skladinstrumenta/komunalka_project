# Generated by Django 4.1.6 on 2023-03-02 05:56

from django.conf import settings
import django.contrib.auth.models
import django.contrib.auth.validators
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='MyUser',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=150, unique=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()], verbose_name='username')),
                ('first_name', models.CharField(blank=True, max_length=150, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('email', models.EmailField(max_length=100, unique=True)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'Пользователь',
                'verbose_name_plural': 'Пользователи',
                'ordering': ['username'],
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='Adress',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('country', models.CharField(max_length=100)),
                ('city', models.CharField(max_length=100)),
                ('street', models.CharField(max_length=255)),
                ('house', models.CharField(max_length=10)),
                ('corps', models.CharField(blank=True, max_length=3, null=True)),
                ('room', models.CharField(blank=True, max_length=10, null=True)),
                ('tarif_gas', models.FloatField(default=1, validators=[django.core.validators.MinValueValidator(0)])),
                ('tarif_delivery_gas', models.FloatField(default=1, validators=[django.core.validators.MinValueValidator(0)])),
                ('tarif_water', models.FloatField(default=1, validators=[django.core.validators.MinValueValidator(0)])),
                ('tarif_light', models.FloatField(default=1, validators=[django.core.validators.MinValueValidator(0)])),
                ('tarif_musor', models.FloatField(default=1, validators=[django.core.validators.MinValueValidator(0)])),
                ('tarif_obsg', models.FloatField(default=1, validators=[django.core.validators.MinValueValidator(0)])),
                ('debt', models.DecimalField(decimal_places=2, default=0, max_digits=10)),
                ('date_create_adress', models.DateTimeField(auto_now_add=True)),
                ('date_update_adress', models.DateTimeField(auto_now=True)),
                ('user', models.ManyToManyField(related_name='users_adress', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Адрес',
                'verbose_name_plural': 'Адреса',
                'ordering': ['country', 'city', 'street', 'house', 'corps', 'room'],
            },
        ),
        migrations.CreateModel(
            name='Repayment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('summ_of_repayment', models.DecimalField(decimal_places=2, default=0, max_digits=10)),
                ('date_of_repayment', models.DateTimeField(auto_now_add=True)),
                ('adress', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app_komunalka.adress', verbose_name='Aдрес')),
            ],
            options={
                'verbose_name_plural': 'Погашения задолженностей',
                'ordering': ['-date_of_repayment'],
            },
        ),
        migrations.CreateModel(
            name='KomunalData',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('gas', models.PositiveIntegerField()),
                ('water', models.PositiveIntegerField()),
                ('light', models.PositiveIntegerField()),
                ('komunaldata_dateon', models.DateField(verbose_name='Дата начала начисления')),
                ('komunaldata_dateoff', models.DateField(verbose_name='Дата завершения начисления')),
                ('date_create', models.DateTimeField(auto_now_add=True)),
                ('date_update', models.DateTimeField(auto_now=True)),
                ('result', models.FloatField(blank=True, null=True, verbose_name='Итого, грн')),
                ('adress', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='adress_komunaldata', to='app_komunalka.adress', verbose_name='Адрес')),
            ],
            options={
                'verbose_name_plural': 'Показания счётчиков',
                'ordering': ['date_update', 'date_create'],
            },
        ),
    ]
