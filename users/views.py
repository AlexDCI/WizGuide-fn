# users/views.py

from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from .forms import UserRegisterForm, UserLoginForm
from django.contrib.auth import get_user_model
import logging
logger = logging.getLogger(__name__)



def logout_view(request):
    """Выход пользователя"""
    logout(request)
    return redirect("main")


def require_login(request):
    return render(request, 'users/require_login.html')

