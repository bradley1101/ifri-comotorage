from django.urls import path

from . import views

app_name = "profil"
urlpatterns = [
    path("", views.mon_profil, name="moi"),
    path("modifier/", views.modifier, name="modifier"),
    path("vehicule/", views.vehicule, name="vehicule"),
    path("<str:username>/", views.public, name="public"),
]
