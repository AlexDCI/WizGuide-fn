# users/forms.py

from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import CustomUser
from django.contrib.auth import authenticate

class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'password1', 'password2']

class UserLoginForm(AuthenticationForm):
    username = forms.CharField(label="Email / Username")

    def clean(self):
        email_or_username = self.cleaned_data.get("username")
        password = self.cleaned_data.get("password")

        if email_or_username and password:
            user = authenticate(username=email_or_username, password=password)
            if user is None:
                try:
                    user_obj = CustomUser.objects.get(email=email_or_username)
                    user = authenticate(username=user_obj.username, password=password)
                except CustomUser.DoesNotExist:
                    pass

            if user is None:
                raise forms.ValidationError("Неверный email/username или пароль")
            
            self.user_cache = user

        return self.cleaned_data
