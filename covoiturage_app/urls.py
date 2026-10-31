from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("", include("accueil_covoiturage_app.urls")),
    path("compte/", include("login.urls")),
    path("profil/", include("profil.urls")),
    path("trajets/", include("trajets.urls")),
    path("offres/", include("publication_offre.urls")),
    path("avis/", include("avis.urls")),
    path("messages/", include("messaging.urls")),
    path("notifications/", include("notifications.urls")),
    path("tableau-de-bord/", include("dashboard.urls")),
    path("admin/", admin.site.urls),
]
