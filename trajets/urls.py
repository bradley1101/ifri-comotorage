from django.urls import path

from . import views

app_name = "trajets"
urlpatterns = [
    path("", views.recherche, name="recherche"),
    path("<int:pk>/", views.detail, name="detail"),
    path("<int:pk>/reserver/", views.reserver, name="reserver"),
    path("reservation/<int:pk>/accepter/", views.accepter, name="accepter"),
    path("reservation/<int:pk>/refuser/", views.refuser, name="refuser"),
    path("reservation/<int:pk>/annuler/", views.annuler, name="annuler"),
]
