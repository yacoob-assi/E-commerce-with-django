from django.urls import path
from .views import signup, loginPage, logoutPage


urlpatterns = [
    path("signup/", signup, name="signup"),
    path("login/", loginPage, name="login"),
    path("logout/", logoutPage, name="logout"),
]
