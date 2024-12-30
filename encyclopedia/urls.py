from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/", views.wiki, name="wiki"),
    path("wiki/<str:entry>", views.entry, name="entry"),
    path("results/<str:query>", views.results, name="results"),
    path("results/wiki/<str:query>", views.reResults, name="reResults"),
    path("new-entry/", views.new_entry, name="new_entry"),
    path("edit-entry/", views.edit, name="edit"),
    path("edit-entry/<str:entry>", views.edit_entry, name="edit_entry"),
    path("wiki/edit-entry/<str:query>", views.re_edit_entry, name="re_edit_entry"),
    path("random-entry-page", views.random_entry_page, name="random_entry_page")
]
