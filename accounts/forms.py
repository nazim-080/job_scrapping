from django import forms
from django.contrib.auth import get_user_model, authenticate
from django.contrib.auth.hashers import check_password

from scrap.models import City, Language

User = get_user_model()


class UserLoginForm(forms.Form):
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)

    def __init__(self, request, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.request = request
        self.user_cache = None

    def clean(self, *args, **kwargs):
        email = self.cleaned_data.get('email').strip()
        password = self.cleaned_data.get('password').strip()

        if email and password:
            qs = User.objects.filter(email=email)
            self.user_cache = authenticate(self.request, email=email, password=password)
            if not qs.exists():
                raise forms.ValidationError('Такого пользователя нет.')
            if not check_password(password, qs[0].password):
                raise forms.ValidationError('Пароль не верный.')
            user = authenticate(email=email, password=password)
            if not user:
                raise forms.ValidationError('Аккаунт отключен.')
        return super(UserLoginForm, self).clean(*args, **kwargs)

    def get_user(self):
        return self.user_cache


class UserRegistrationForm(forms.ModelForm):
    email = forms.EmailField(label='Введите email')
    password = forms.CharField(widget=forms.PasswordInput, label='Введите пароль')
    password2 = forms.CharField(widget=forms.PasswordInput, label='Повторите пароль')

    class Meta:
        model = User
        fields = ('email',)

    def clean_password2(self):
        data = self.cleaned_data
        if data['password'] != data['password2']:
            raise forms.ValidationError('Пароли не совпадают')
        return data['password2']


class UserUpdateForm(forms.ModelForm):
    city = forms.ModelChoiceField(queryset=City.objects.all(), label='Город', to_field_name='slug', required=True)
    language = forms.ModelChoiceField(queryset=Language.objects.all(), label='Специальность',
                                      to_field_name='slug', required=True)
    send_email = forms.BooleanField(required=False, label='Получать рассылку?')

    class Meta:
        model = User
        fields = {'city', 'language', 'send_email'}
