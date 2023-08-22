from django.urls import path

from app_komunalka.views import *

urlpatterns = [
    path('', HomePage.as_view(), name='home'),
    path('komunal_data/create', CreateNewKomubalDataView.as_view(), name='new_data'),
    path('adress/list', AdressListView.as_view(), name='adress_list'),
    path('adress/create', AdressCreateView.as_view(), name='new_adress'),
    path('adress/update/<int:pk>', AdressUpdateView.as_view(), name='adress_update'),
    path('index', IndexPage.as_view(), name='index'),
    path('register', RegistrationNewUserView.as_view(), name='register'),
    path('login', LoginUser.as_view(), name='login'),
    path('logout', LogoutUser.as_view(), name='logout'),
    path('komunal_data', KomunalDataListView.as_view(), name='kd_list'),
    path('komunal_data/update/<int:pk>', UpdateKomunalData.as_view(), name='update_kdata'),
    path('komunal_data/delete/<int:pk>', DeleteKomunalData.as_view(), name='delete_kdata'),
    path('repayment/create/', RepaymentCreateView.as_view(), name='repayment_create')


    ]
