from django.contrib import admin

from app_komunalka.models import MyUser, Adress, KomunalData, Repayment


# class ChooseAdressesAdmin(admin.ModelAdmin):
#     filter_horizontal = ['adress']


class ChooseUsersAdmin(admin.ModelAdmin):
    filter_horizontal = ['user']


admin.site.register(MyUser)
admin.site.register(Adress, ChooseUsersAdmin)
admin.site.register(KomunalData)
admin.site.register(Repayment)




