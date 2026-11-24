import re
from PIL import Image
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.core.validators import FileExtensionValidator
from .models import CustomUser, Application, Category
import os


def validate_custom_image(image):
    if image.size > 2 * 1024 * 1024:
        raise forms.ValidationError('Размер файла не должен превышать 2 МБ')

    ext = os.path.splitext(image.name)[1].lower()
    if ext not in ['.jpg', '.jpeg', '.png', '.bmp']:
        raise forms.ValidationError('Разрешены только форматы JPG, JPEG, PNG и BMP')

    img = Image.open(image)
    if img.format not in ['JPEG', 'PNG', 'BMP']:
        raise forms.ValidationError('Разрешены только форматы JPG, JPEG, PNG и BMP')
    image.seek(0)


image_ext_validator = FileExtensionValidator(
    allowed_extensions=['jpg', 'jpeg', 'png', 'bmp'],
    message='Разрешены только файлы с расширением JPG, JPEG, PNG и BMP'
)


class RegistrationForm(UserCreationForm):
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
        if not re.match(r'^[А-Яа-яЁё\s-]+$', full_name):
            raise forms.ValidationError('ФИО может содержать только кириллические буквы, дефис и пробелы')
        return full_name

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if not re.match(r'^[A-Za-z-]+$', username):
            raise forms.ValidationError('Логин может содержать только буквы латиницы и дефис')
        if CustomUser.objects.filter(username=username).exists():
            raise forms.ValidationError('Такой логин уже существует')
        return username


class ApplicationForm(forms.ModelForm):
    image = forms.ImageField(
        label="Фото или план помещения",
        required=True,
        validators=[validate_custom_image],
        error_messages={'invalid_image': "Недопустимый формат изображения"}
    )

    class Meta:
        model = Application
        fields = ('title', 'description', 'category', 'image')


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
    design_image = forms.ImageField(
        label="Дизайн",
        required=True,
        validators=[validate_custom_image],
        error_messages={'invalid_image': "Недопустимый формат изображения"}
    )

    class Meta:
        model = Application
        fields = ('design_image',)
