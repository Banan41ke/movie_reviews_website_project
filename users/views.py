# users/views.py
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import login, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from .forms import RegisterForm, UserUpdateForm, ProfileUpdateForm, CustomPasswordChangeForm
from .models import Profile
from movies.models import Review, Comment  # Импорт из приложения movies


# def register_view(request):
#     if request.method == "POST":
#         form = RegisterForm(request.POST)
#         if form.is_valid():
#             user = form.save()
#             login(request, user)
#             messages.success(request, "Регистрация прошла успешно! Добро пожаловать!")
#             return redirect("movie_list")
#     else:
#         form = RegisterForm()

#     return render(request, "users/register.html", {"form": form})

def register_view(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            
            # Создаем профиль для нового пользователя
            Profile.objects.create(user=user)
            
            # Авторизуем пользователя
            login(request, user)
            
            messages.success(request, "Регистрация прошла успешно!")
            return redirect("movie_list")
    else:
        form = UserCreationForm()
    
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


# @login_required
# def edit_profile_view(request):
#     if request.method == 'POST':
#         # Обновление email
#         new_email = request.POST.get('email')
#         if new_email and new_email != request.user.email:
#             from django.contrib.auth.models import User
#             if not User.objects.filter(email=new_email).exists():
#                 request.user.email = new_email
#                 request.user.save()
#                 messages.success(request, 'Email успешно обновлен!')
#             else:
#                 messages.error(request, 'Этот email уже используется другим пользователем.')

#         # Обновление информации профиля
#         profile = request.user.profile
#         profile.bio = request.POST.get('bio', '')
#         profile.save()
#         messages.success(request, 'Профиль успешно обновлен!')
#         return redirect('profile')

@login_required
def edit_profile(request):
    if request.method == 'POST':
        user_form = UserUpdateForm(request.POST, instance=request.user)
        profile_form = ProfileUpdateForm(
            request.POST, 
            request.FILES, 
            instance=request.user.profile
        )
        
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Ваш профиль успешно обновлен!')
            return redirect('profile')
    else:
        user_form = UserUpdateForm(instance=request.user)
        profile_form = ProfileUpdateForm(instance=request.user.profile)
    
    context = {
        'user_form': user_form,
        'profile_form': profile_form,
    }
    return render(request, 'users/edit_profile.html', context)

@login_required
def change_password(request):
    if request.method == 'POST':
        form = CustomPasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            # Обновляем сессию, чтобы пользователь не разлогинился
            update_session_auth_hash(request, user)
            messages.success(request, 'Ваш пароль успешно изменен!')
            return redirect('profile')
    else:
        form = CustomPasswordChangeForm(request.user)
    
    context = {'form': form}
    return render(request, 'users/change_password.html', context)