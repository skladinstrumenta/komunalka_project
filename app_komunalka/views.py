from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.views import LoginView, LogoutView
from django.core.exceptions import ValidationError
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import TemplateView, CreateView, FormView, ListView, UpdateView, DeleteView
from django.views.generic.edit import ModelFormMixin

from app_komunalka.forms import UserCreateForm, LoginForm, DataCreateForm, NewAdressForm, DataUpdateForm
from app_komunalka.models import MyUser, KomunalData, Adress, Repayment


class HomePage(TemplateView):
    template_name = 'home.html'
    

# class AddUserInFormMixin(UpdateView):
#     def get_form_kwargs(self):
#         kwargs = super().get_form_kwargs()
#         kwargs.update(user=self.request.user)
#         return kwargs

class AddUserInFormMixin(ModelFormMixin):
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs.update(user=self.request.user)
        return kwargs


class IndexPage(TemplateView):
    template_name = 'index.html'


class RegistrationNewUserView(CreateView):
    template_name = "registration.html"
    form_class = UserCreateForm
    success_url = '/'

    def form_valid(self, form):
        valid = super().form_valid(form)
        user = form.save()
        login(self.request, user)
        return valid


# class LoginUser(FormView):
#     template_name = 'login.html'
#     form_class = LoginForm
#     next_page = "home"
#
#     def form_valid(self, form):
#         email = form.cleaned_data.get('email')
#         user = MyUser.objects.filter(email=email)
#         # user = authenticate(username=username, password=password)
#         login(self.request, user)
#         return super().form_valid(form)


class LoginUser(LoginView):
    template_name = "login.html"
    form_class = LoginForm
    next_page = "home"
    extra_context = {'login_form': LoginForm}

    def get_context_data(self, **kwargs):
        context = super(LoginUser, self).get_context_data(**kwargs)
        return dict(list(context.items()))


class LogoutUser(LogoutView):
    next_page = '/'


class KomunalDataListView(ListView):
    model = KomunalData
    template_name = 'komunaldata.html'
    context_object_name = 'data_list'
    paginate_by = 3
    # new_obj = KomunalData.objects.all()[0]
    # last_obj = KomunalData.objects.all()[1]
    # diference_obj = {'gas': (new_obj.gas - last_obj.gas),
    #                  'water': (new_obj.water - last_obj.water),
    #                  'light': (new_obj.light - last_obj.light)}
    #
    # extra_context = {'dif_obj': diference_obj}


    def get_queryset(self):
        # if not self.request.user.is_superuser:
        #     queryset = KomunalData.objects.filter(adress__user=self.request.user)
        #     return queryset
        # queryset = KomunalData.objects.all()
        queryset = KomunalData.objects.filter(adress__user=self.request.user)
        return queryset

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(KomunalDataListView, self).get_context_data(**kwargs)
        user = self.request.user
        queryset = self.get_queryset()
        if len(queryset) > 1:
            kol = len(queryset)
            # index =
            # index_new_obj = list(queryset).index()
            index_new_obj = 0
            # index_new_obj = queryset.index()
            obj = queryset[index_new_obj]
            # obj_n = queryset.get(id=object_list.first())
            next_obj = queryset[index_new_obj + 1]
            diference_obj = {'gas': (obj.gas - next_obj.gas),
                             'water': (obj.water - next_obj.water),
                             'light': (obj.light - next_obj.light)}
            context['dif_obj'] = diference_obj
        return context


class CreateNewKomubalDataView(AddUserInFormMixin, CreateView):
    # model = KomunalData
    template_name = 'NewData.html'
    form_class = DataCreateForm
    success_url = reverse_lazy('kd_list')

    def form_valid(self, form):
        obj = form.save(commit=False)
        adress_id = obj.adress.id
        adress_obj = Adress.objects.get(pk=adress_id)
        qyeryset = KomunalData.objects.filter(adress=adress_obj)
        if qyeryset:
            last_obj = qyeryset.first()
            diference_gas = obj.gas - last_obj.gas
            diference_water = obj.water - last_obj.water
            diference_light = obj.light - last_obj.light
            sum_gas = diference_gas * adress_obj.tarif_gas + adress_obj.tarif_delivery_gas
            if sum_gas < 0:
                raise ValidationError("New Gas < Last Gas")
            sum_water = diference_water * adress_obj.tarif_water
            sum_light = diference_light * adress_obj.tarif_light
            result_list = [sum_gas, sum_water, sum_light, adress_obj.tarif_musor, adress_obj.tarif_obsg]
            obj.result = round(sum(result_list), 2)
        else:
            obj.result = 0
        obj.save()
        
        return super(CreateNewKomubalDataView, self).form_valid(form)


class UpdateKomunalData(AddUserInFormMixin, UpdateView):
    model = KomunalData
    form_class = DataUpdateForm
    template_name = "update_kdata.html"
    success_url = reverse_lazy('kd_list')


class DeleteKomunalData(DeleteView):
    model = KomunalData
    success_url = reverse_lazy('kd_list')


class AdressListView(ListView):
    model = Adress
    template_name = 'adresslist.html'
    context_object_name = 'adress_list'

    def get_queryset(self):
        queryset = Adress.objects.filter(user=self.request.user)
        return queryset


class AdressCreateView(CreateView):
    template_name = 'Newadress.html'
    form_class = NewAdressForm
    success_url = '/'


class AdressUpdateView(UpdateView):
    model = Adress
    form_class = NewAdressForm
    template_name = 'update_adress.html'
    # fields = '__all__'
    success_url = reverse_lazy('home')


class RepaymentCreateView(CreateView):
    template_name = 'Newrepayment.html'
    model = Repayment
    fields = '__all__'
    success_url = '/'
