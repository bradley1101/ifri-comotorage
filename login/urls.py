from django.urls import path

from . import views

app_name = "login"
urlpatterns = [
    path("connexion/", views.Connexion.as_view(), name="connexion"),
    path("deconnexion/", views.Deconnexion.as_view(), name="deconnexion"),
    path("inscription/", views.inscription, name="inscription"),
]
