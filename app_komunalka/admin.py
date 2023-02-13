from django.contrib import admin

from app_komunalka.models import MyUser, Adress


class ChooseAdressesAdmin(admin.ModelAdmin):
    filter_horizontal = ['adress']


class ChooseUsersAdmin(admin.ModelAdmin):
    filter_horizontal = ['user']


admin.site.register(MyUser, ChooseAdressesAdmin)
admin.site.register(Adress, ChooseUsersAdmin)




