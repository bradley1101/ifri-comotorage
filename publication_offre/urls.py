from django.urls import path

from . import views

app_name = "publication_offre"
urlpatterns = [
    path("nouvelle/", views.nouvelle, name="nouvelle"),
    path("<int:pk>/modifier/", views.modifier, name="modifier"),
    path("<int:pk>/annuler/", views.annuler, name="annuler"),
]
