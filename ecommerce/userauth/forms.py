from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User


class user_signup_form(UserCreationForm):

    username = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "placeholder": "Username",
                "class": "form-control mb-3",
                "id": "exampleInputtext1",
            }
        )
    )
    email = forms.EmailField(
        widget=forms.EmailInput(
            attrs={
                "placeholder": "Email",
                "class": "form-control mb-3",
                "id": "exampleInputEmail1",
            }
        )
    )
    password1 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "placeholder": "Password",
                "class": "form-control mb-4",
                "id": "exampleInputPassword1",
            }
        )
    )
    password2 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "placeholder": "Confirm Password",
                "class": "form-control mb-4",
            }
        )
    )

    class Meta:
        model = User
        fields = ["email", "username"]
