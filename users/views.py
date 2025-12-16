# users/views.py
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from .forms import RegisterForm
from movies.models import Review, Comment  # Импорт из приложения movies


def register_view(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Регистрация прошла успешно! Добро пожаловать!")
            return redirect("movie_list")
    else:
        form = RegisterForm()

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
def edit_profile_view(request):
    if request.method == 'POST':
        # Обновление email
        new_email = request.POST.get('email')
        if new_email and new_email != request.user.email:
            from django.contrib.auth.models import User
            if not User.objects.filter(email=new_email).exists():
                request.user.email = new_email
                request.user.save()
                messages.success(request, 'Email успешно обновлен!')
            else:
                messages.error(request, 'Этот email уже используется другим пользователем.')

        # Обновление информации профиля
        profile = request.user.profile
        profile.bio = request.POST.get('bio', '')
        profile.save()
        messages.success(request, 'Профиль успешно обновлен!')
        return redirect('profile')

    return render(request, "users/edit_profile.html")