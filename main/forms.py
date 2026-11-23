import re
import os
from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser, Application, Category

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
class ApplicationForm(forms.ModelForm):
    class Meta:
        model = Application
        fields = ('title', 'description', 'category', 'image')

        def clean_image(self):
            image = self.cleaned_data.get('image')
            if image:
                ext = os.path.splitext(image)[1].lower()
                if ext not in ['.jpg', '.jpeg', '.png', '.bmp']:
                    raise forms.ValidationError('Недопустимый формат изображения')
                if image.size > 2 * 1024 * 1024:
                    raise forms.ValidationError('Размер файла не должен превышать 2 МБ')
            return image
class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ('name',)

class InProgressForm(forms.ModelForm):
    comment = forms.CharField(label="Комментарий администратора", widget=forms.Textarea, required=True)

    class Meta:
        model = Application
        fields = ('comment',)

class CompletedForm(forms.ModelForm):
    design_image = forms.ImageField(label="Дизайн", required=True)

    class Meta:
        model = Application
        fields = ('design_image',)

        def clean_design_image(self):
            image = self.cleaned_data.get('design_image')
            if image:
                ext = os.path.splitext(image)[1].lower()
                if ext not in ['.jpg', '.jpeg', '.png', '.bmp']:
                    raise forms.ValidationError('Недопустимый формат изображения')
                if image.size > 2 * 1024 * 1024:
                    raise forms.ValidationError('Размер файла не должен превышать 2 МБ')
            return image