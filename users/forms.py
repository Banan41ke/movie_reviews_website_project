# users/forms.py
from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, PasswordChangeForm
from django.contrib.auth.models import User
from .models import Profile

class UserUpdateForm(UserChangeForm):
    email = forms.EmailField(required=False)
    first_name = forms.CharField(required=False, label='Имя')
    last_name = forms.CharField(required=False, label='Фамилия')
    
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name']
        help_texts = {
            'username': None,  # убираем стандартную подсказку
        }

class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['avatar', 'bio', 'location', 'website', 'birth_date']
        widgets = {
            'bio': forms.Textarea(attrs={'rows': 4}),
            'birth_date': forms.DateInput(attrs={'type': 'date'}),
        }
        labels = {
            'avatar': 'Аватар',
            'bio': 'О себе',
            'location': 'Местоположение',
            'website': 'Веб-сайт',
            'birth_date': 'Дата рождения',
        }

class CustomPasswordChangeForm(PasswordChangeForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Кастомизация полей если нужно
        self.fields['old_password'].label = 'Старый пароль'
        self.fields['new_password1'].label = 'Новый пароль'
        self.fields['new_password2'].label = 'Подтвердите новый пароль'        

class RegisterForm(UserCreationForm):
    email = forms.EmailField(
        required=True,
        label="Email",
        widget=forms.EmailInput(attrs={
            "placeholder": "Email"
        }),
        help_text="Введите ваш email"
    )

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")
        widgets = {
            "username": forms.TextInput(attrs={
                "placeholder": "Имя пользователя"
            }),
            "password1": forms.PasswordInput(attrs={
                "placeholder": "Пароль"
            }),
            "password2": forms.PasswordInput(attrs={
                "placeholder": "Подтверждение пароля"
            }),
        }
        help_texts = {
            'username': 'Максимум 150 символов. Только буквы, цифры и символы @/./+/-/_',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password2'].help_text = 'Повторите пароль для подтверждения'

    def clean_email(self):
        email = self.cleaned_data.get("email")
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("Пользователь с таким email уже существует")
        return email

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data["email"]
        if commit:
            user.save()
        return user