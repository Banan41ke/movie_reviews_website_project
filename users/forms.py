# users/forms.py
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm
from .models import Profile

# Простая форма регистрации
class SimpleRegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)
    
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

# Простая форма обновления пользователя
class SimpleProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['avatar', 'bio']
        widgets = {
            'bio': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Расскажите немного о себе…',
                'rows': 4
            }),
            'avatar': forms.FileInput(attrs={
                'class': 'form-control'
            }),
        }
        help_texts = {
            'bio': 'Этот текст будет отображаться в вашем профиле',
            'avatar': 'PNG / JPG до 2 МБ',
        }



# Простая форма обновления профиля
class SimpleUserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email']
        widgets = {
            'username': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Введите имя пользователя'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'email@example.com'
            }),
        }
        help_texts = {
            'username': 'Это имя будет видно другим пользователям',
            'email': 'Необязательно',
        }


# Простая форма смены пароля
class SimplePasswordChangeForm(PasswordChangeForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({'class': 'form-control'})