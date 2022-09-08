from django.urls import path

from . import views

app_name = "encyclopedia"

urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/<str:entry>", views.entry, name="entry"),
    path("search_entry",views.search_entry, name="search_entry"),
    path("new_entry", views.new_entry, name="new_entry"),
    path ("wiki/<str:entry>/edit", views.edit , name="edit"),
    path("random", views.random, name="random")
]
