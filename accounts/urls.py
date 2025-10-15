# accounts/urls.py
from django.urls import path
from .views import RegisterView, UserLoginView, UserLogoutView, ProfileView

from django.contrib.auth.views import LogoutView

from .views import user_logout

app_name = "accounts"

urlpatterns = [
    path("register/", RegisterView.as_view(), name="register"),
    path("login/", UserLoginView.as_view(), name="login"),
    path("logout/", user_logout, name="logout"),
    path("profile/", ProfileView.as_view(), name="profile"),
]
