# users/urls.py


from django.urls import path
from .views import register_view, login_view, logout_view, require_login

urlpatterns = [
    path("register/", register_view, name="register"),
    path("login/", login_view, name="login"),
    path("logout/", logout_view, name="logout"),
    path("require-login/", require_login, name='require_login'),
]
