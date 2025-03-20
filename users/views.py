# users/views.py

from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from .forms import UserRegisterForm, UserLoginForm
from django.contrib.auth import get_user_model
import logging
logger = logging.getLogger(__name__)

def register_view(request):
    """Регистрация пользователя"""
    if request.method == "POST":
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Явно указываем backend после создания пользователя
            user.backend = 'django.contrib.auth.backends.ModelBackend'  # Используем стандартный backend
            login(request, user)
            return redirect("main")  # Перенаправляем на главную страницу
    else:
        form = UserRegisterForm()
    return render(request, "users/register.html", {"form": form})


def login_view(request):
    """Авторизация пользователя"""
    if request.method == "POST":
        form = UserLoginForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect("main")  # Перенаправляем на главную страницу
    else:
        form = UserLoginForm()
    return render(request, "users/login.html", {"form": form})

def logout_view(request):
    """Выход пользователя"""
    logout(request)
    return redirect("main")


def require_login(request):
    return render(request, 'users/require_login.html')

