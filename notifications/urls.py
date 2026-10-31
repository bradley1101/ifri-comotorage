from django.urls import path

from . import views

app_name = "notifications"
urlpatterns = [
    path("", views.liste, name="liste"),
    path("<int:pk>/", views.ouvrir, name="ouvrir"),
    path("tout-lire/", views.tout_lire, name="tout_lire"),
    path("api/compteur/", views.api_compteur, name="api_compteur"),
]
