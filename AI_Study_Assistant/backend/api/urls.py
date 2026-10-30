from django.urls import path
from . import views

urlpatterns = [
    path("health/", views.health_check, name="health_check"),
    path("notes/generate/", views.generate_note, name="generate_note"),
    path("notes/generate-from-file/", views.generate_note_from_file, name="generate_note_from_file"),
]