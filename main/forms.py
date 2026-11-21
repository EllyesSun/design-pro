import re
from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser

class RegistationForm(UserCreationForm):
    full_name = forms.CharField(label='ФИО', required=True)
    username = forms.CharField(label='Логин', required=True)
    email = forms.EmailField(label='Email', required=True)
    agree = forms.BooleanField(label='Согласие на обработку персональных данных', required=True, initial=True)
    password1 = forms.CharField(label='Пароль', widget=forms.PasswordInput, help_text="", required=True)
    password2 = forms.CharField(label='Подтверждение пароля', widget=forms.PasswordInput, help_text="", required=True)

    class Meta:
        model = CustomUser
        fields = ('full_name', 'username', 'email')

        def clean_full_name(self):
            full_name = self.cleaned_data.get('full_name')
            if not re.match(r'^[A-Za-z]+$', full_name):
                raise forms.ValidationError('ФИО может содержать только кириллические буквы, дефис и пробелы')
            return full_name

        def clean_username(self):
            username = self.cleaned_data.get('username')
            if not re.match(r'^[A-Za-z]+$', username):
                raise forms.ValidationError('ФИО может содержать только буквы латиницы и дефис')
            if CustomUser.objects.filter(username=username).exists():
                raise forms.ValidationError('Такой логин уже существует')
            return username