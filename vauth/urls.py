from django.urls import path, include
from .views import *


app_name="vauth"
urlpatterns = [
    path("signup/", signup, name="signup"),
    path("login/", login, name="login"),
    path("logout/", logout, name="logout"),
]