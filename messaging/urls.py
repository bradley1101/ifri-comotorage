from django.urls import path

from . import views

app_name = "messaging"
urlpatterns = [
    path("", views.boite, name="boite"),
    path("avec/<str:username>/", views.demarrer, name="demarrer"),
    path("<int:pk>/", views.conversation, name="conversation"),
    path("api/<int:pk>/", views.api_messages, name="api_messages"),
    path("api/<int:pk>/envoyer/", views.api_envoyer, name="api_envoyer"),
]
