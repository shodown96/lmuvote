from django.urls import path, include
from .views import *


app_name="polls"
urlpatterns = [
    path("", index, name="index"),
    path("categories/", categories, name="categories"),
    path("category/", category, name="category"),
    path("vote/", vote, name="vote"),
    path("results/", results, name="results"),
    path("contact/", contact, name="contact"),
]