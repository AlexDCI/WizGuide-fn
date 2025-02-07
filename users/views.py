# users/views.py

from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from .forms import UserRegisterForm, UserLoginForm

def register_view(request):
    """Регистрация пользователя"""
    if request.method == "POST":
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("main")  # Перенаправляем на главную страницу
    else:
        form = UserRegisterForm()
    return render(request, "main/register.html", {"form": form})

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
    return render(request, "main/login.html", {"form": form})

def logout_view(request):
    """Выход пользователя"""
    logout(request)
    return redirect("main")
