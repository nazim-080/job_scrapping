from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib import messages
from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView, UpdateView

from .forms import UserLoginForm, UserRegistrationForm, UserUpdateForm
from .models import MyUser

User = get_user_model()


class LoginUser(LoginView):
    form_class = UserLoginForm
    template_name = 'accounts/login.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

    def get_success_url(self):
        return reverse_lazy('home')


def logout_user(request):
    logout(request)
    return redirect('home')


class RegisterUser(CreateView):
    form_class = UserRegistrationForm
    template_name = 'accounts/register.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

    def form_valid(self, form):
        user = form.save()
        messages.success(self.request, 'Пользователь зарегестрирован.')
        return render(self.request, 'accounts/register_done.html', {'new_user': user})


class UserUpdate(LoginRequiredMixin, UpdateView):
    model = MyUser
    template_name = 'accounts/update.html'
    pk_url_kwarg = 'user_pk'
    form_class = UserUpdateForm

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        form = UserUpdateForm(initial={'city': self.request.user.city,
                                       'language': self.request.user.language,
                                       'send_email': self.request.user.send_email})
        context['form'] = form
        return context

    def post(self, request, *args, **kwargs):
        form = UserUpdateForm(request.POST)
        user = request.user
        if form.is_valid():
            data = form.cleaned_data
            user.city = data['city']
            user.language = data['language']
            user.send_email = data['send_email']
            user.save()
            messages.success(request, 'Настройки сохранены.')
        return redirect(f'accounts:update', user_pk=user.pk)


def delete_view(request):
    if request.user.is_authenticated:
        user = request.user
        if request.method == 'POST':
            qs = User.objects.get(pk=user.pk)
            qs.delete()
            messages.error(request, 'Пользователь удален.')
    return redirect('home')

