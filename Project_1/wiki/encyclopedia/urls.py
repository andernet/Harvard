from django.urls import path

from . import views

app_name = "encyclopedia"
urlpatterns = [
    path("", views.index, name="index"),
    path("new_entry", views.new_entry, name="new_entry"),
    path("edit", views.edit, name="edit"),
    path("error", views.error, name="error"),
    path("random_entry", views.random_entry, name="random_entry"),
    path("wiki/<str:title>", views.entry, name="entry"),
]
