from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/<str:title>", views.article, name="article"),
    path("search", views.search, name="search"),
    path("random", views.random, name="random"),
    path("add", views.add, name="add"),
    path("save", views.save, name="save"),
    path("wiki/<str:title>/edit", views.edit, name="edit"),
]
