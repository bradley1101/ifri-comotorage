from django.urls import path

from . import views

app_name = "avis"
urlpatterns = [path("trajet/<int:trajet_pk>/<str:username>/", views.noter, name="noter")]
