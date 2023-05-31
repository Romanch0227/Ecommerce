from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="blogHome"),
    path("POST/<int:id>", views.POST, name="blogpost")
]
