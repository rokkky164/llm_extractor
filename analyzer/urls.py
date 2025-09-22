from django.urls import path
from .views import analyze, search


urlpatterns = [
    path("analyze", analyze, name="analyze"),
    path("search", search, name="search"),
]