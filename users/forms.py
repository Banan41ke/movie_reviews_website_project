# users/forms.py
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


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