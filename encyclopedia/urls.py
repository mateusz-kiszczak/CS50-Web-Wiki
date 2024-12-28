from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/", views.wiki, name="wiki"),
    path("wiki/<str:entry>", views.entry, name="entry"),
    path("results/<str:query>", views.results, name="results"),
    path("results/wiki/<str:query>", views.reResults, name="reResults"),
    path("newEntry", views.newEntry, name="newEntry")
]
