from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from .forms import RegisterForm, LoginForm

def login_view(request):
    form = LoginForm(request, data=request.POST or None)
    if request.method == "POST" and form.is_valid():
        login(request, form.get_user())
        return redirect("movie_list")
    return render(request, "users/login.html", {"form": form})

def register_view(request):
    form = RegisterForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        user = form.save(commit=False)
        user.set_password(form.cleaned_data["password"])
        user.save()
        messages.success(request, "Регистрация прошла успешно")
        return redirect("login")
    return render(request, "users/register.html", {"form": form})

def logout_view(request):
    logout(request)
    return redirect("movie_list")
