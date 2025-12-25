# users/views.py
from django.contrib.auth import logout as auth_logout
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm
from .models import Profile
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import login, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from .forms import SimpleRegisterForm, SimpleUserUpdateForm, SimpleProfileUpdateForm, SimplePasswordChangeForm  
from movies.models import Favorite, Review, Comment


def custom_logout(request):
    """Кастомный выход с редиректом на главную"""
    auth_logout(request)
    return redirect('movie_list')  # или 'home', смотря как называется ваша главная

@login_required
def change_password(request):
    if request.method == 'POST':
        old_password = request.POST.get('old_password')
        new_password1 = request.POST.get('new_password1')
        new_password2 = request.POST.get('new_password2')
        
        # Проверяем, что все поля заполнены
        if not all([old_password, new_password1, new_password2]):
            messages.error(request, 'Все поля обязательны для заполнения')
            return redirect('change_password')
        
        # Проверяем правильность старого пароля
        user = request.user
        if not user.check_password(old_password):
            messages.error(request, 'Текущий пароль введен неверно')
            return redirect('change_password')
        
        # Проверяем совпадение новых паролей
        if new_password1 != new_password2:
            messages.error(request, 'Новые пароли не совпадают')
            return redirect('change_password')
        
        # Проверяем длину пароля
        if len(new_password1) < 8:
            messages.error(request, 'Пароль должен содержать минимум 8 символов')
            return redirect('change_password')
        
        # Меняем пароль
        user.set_password(new_password1)
        user.save()
        
        # Обновляем сессию
        update_session_auth_hash(request, user)
        
        messages.success(request, 'Пароль успешно изменен!')
        return redirect('profile')
    
    return render(request, 'users/change_password.html')

@login_required
def my_reviews(request):
    """Страница с моими отзывами"""
    reviews = Review.objects.filter(user=request.user).select_related('movie').order_by('-created_at')
    
    context = {
        'reviews': reviews,
        'reviews_count': reviews.count(),
    }
    return render(request, 'users/my_reviews.html', context)

@login_required
def favorites(request):
    """Страница с избранными фильмами"""
    favorites = Favorite.objects.filter(user=request.user).select_related('movie').order_by('-created_at')
    
    context = {
        'favorites': favorites,
        'favorites_count': favorites.count(),
    }
    return render(request, 'users/favorites.html', context)

def register_view(request):
    if request.method == "POST":
        form = SimpleRegisterForm(request.POST)  # Используйте SimpleRegisterForm
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Регистрация прошла успешно!")
            return redirect("movie_list")
    else:
        form = SimpleRegisterForm()
    
    return render(request, "users/register.html", {"form": form})



@login_required
def profile_view(request):
    user = request.user
    reviews = Review.objects.filter(user=user).select_related('movie').order_by('-created_at')
    comments = Comment.objects.filter(user=user).select_related('movie').order_by('-created_at')

    context = {
        'user': user,
        'reviews': reviews,
        'comments': comments,
        'reviews_count': reviews.count(),
        'comments_count': comments.count(),
    }
    return render(request, "users/profile.html", context)

@login_required
def edit_profile(request):
    user = request.user
    profile = user.profile

    if request.method == 'POST':
        user_form = SimpleUserUpdateForm(request.POST, instance=user)
        profile_form = SimpleProfileUpdateForm(request.POST, request.FILES, instance=profile)

        print("=== DEBUG ===")
        print("POST data:", request.POST)
        print("FILES data:", request.FILES)
        print("user_form valid:", user_form.is_valid())
        print("profile_form valid:", profile_form.is_valid())
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            print("=== SAVED ===")
            messages.success(request, 'Профиль обновлён!')
            return redirect('profile')
        else:
            print("user_form errors:", user_form.errors)
            print("profile_form errors:", profile_form.errors)

    else:
        user_form = SimpleUserUpdateForm(instance=user)
        profile_form = SimpleProfileUpdateForm(instance=profile)

    return render(request, 'users/edit_profile.html', {
        'user_form': user_form,
        'profile_form': profile_form,
    })