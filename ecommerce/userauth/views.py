from django.shortcuts import render, redirect
from .forms import user_signup_form
from django.contrib.auth import authenticate, login, logout
from .models import User
from django.contrib import messages
from django.urls import reverse

# Create your views here.


def signup(request):
    if request.method == "POST":
        form = user_signup_form(request.POST)
        if form.is_valid():
            new_user = form.save(commit=False)
            new_user.set_password(form.cleaned_data["password1"])
            new_user.save()

            user = authenticate(
                username=new_user.email, password=form.cleaned_data["password1"]
            )
            if user is not None:
                login(request, user)
                return redirect("index")
    else:
        form = user_signup_form()
    return render(request, "signup.html", {"form": form})


def loginPage(request):
    if request.user.is_authenticated:
        return redirect(reverse("index"))

    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")

        try:
            user = User.objects.get(email=email)
        except:
            messages.error(request, f"User with {email} does not exist")

        user = authenticate(request, email=email, password=password)

        if user is not None:
            login(request, user)
            messages.success(request, "You are logged in")
            return redirect(reverse("index"))

        else:
            messages.error(request, "User does not exist")
    return render(request, "login.html")


def logoutPage(request):
    logout(request)
    messages.warning(request, "you are logged out")
    return redirect("login")
