from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/<str:title>/", views.page, name="page"),
    path("error", views.error, name="error"),
    path("search", views.search, name="search"),
    path("new", views.new_page, name="new-page"),
    path("save", views.save, name="save"),
    path("edit/<str:title>/", views.edit_page, name="edit-page"),
    path("save-edit", views.save_edit, name="save-edit"),
    path("random-page", views.random_page, name="random-page"),
]
