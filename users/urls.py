# users/urls.py
from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    # Регистрация
    path("register/", views.register_view, name="register"),
    
    # Профиль
    path("profile/", views.profile_view, name="profile"),
    path("profile/edit/", views.edit_profile, name="edit_profile"),
    path("profile/change-password/", views.change_password, name="change_password"),  # ← ДОБАВЬТЕ ЭТУ СТРОКУ!
    
    # Вход/выход
    path("login/", auth_views.LoginView.as_view(
        template_name="users/login.html",
        redirect_authenticated_user=True
    ), name="login"),
    
    path("logout/", auth_views.LogoutView.as_view(
        next_page="/"
    ), name="logout"),
]