from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.views import LoginView, LogoutView
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import TemplateView, CreateView, FormView, ListView
from app_komunalka.forms import UserCreateForm, LoginForm, DataCreateForm
from app_komunalka.models import MyUser, KomunalData


class HomePage(TemplateView):
    template_name = 'home.html'


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
    paginate_by = 5


class CreateNewKomubalDataView(CreateView):
    model = KomunalData
    template_name = 'NewData.html'
    # form_class = DataCreateForm
    model = KomunalData
    fields = ['gas', 'water', 'light', 'adress', 'komunaldata_dateon', 'komunaldata_dateoff']
    success_url = reverse_lazy('kd_list')


