"""python manage.py seed_demo  — fictitious members, rides, bookings, reviews and messages.

All demo accounts use the password  ifri2025demo
"""
from datetime import timedelta

from django.core.management.base import BaseCommand
from django.db import transaction
from django.utils import timezone

from avis.models import Avis
from messaging.models import Message
from messaging.views import conversation_entre
from profil.models import Vehicule
from trajets import services
from trajets.models import Reservation, Trajet
from users.models import User

PASSWORD = "ifri2025demo"
LIEUX = {
    "IFRI": ("IFRI — UAC Abomey-Calavi", 6.4183, 2.3417),
    "godomey": ("Carrefour Godomey", 6.3866, 2.3497),
    "kpota": ("Calavi Kpota", 6.4485, 2.3550),
    "etoile": ("Cotonou — Étoile Rouge", 6.3745, 2.4120),
    "akpakpa": ("Akpakpa — Carrefour Sègbèya", 6.3615, 2.4510),
    "fidjrosse": ("Fidjrossè Plage", 6.3575, 2.3650),
    "togba": ("Togba", 6.4560, 2.3150),
    "zogbadje": ("Zogbadjè", 6.4140, 2.3380),
    "cadjehoun": ("Cadjèhoun", 6.3570, 2.3900),
}
MEMBRES = [
    ("koffi", "Koffi", "Adjovi", "SEIOT", "conducteur", ("Toyota", "Corolla", "grise", 3)),
    ("rita", "Rita", "Agossou", "GL", "les_deux", ("Suzuki", "Swift", "rouge", 3)),
    ("marc", "Marc", "Dossou", "IA", "conducteur", ("Bajaj", "Boxer (moto)", "noire", 1)),
    ("awa", "Awa", "Sossa", "SEIOT", "passager", None),
    ("jean", "Jean", "Houngbo", "SI", "passager", None),
    ("ella", "Ella", "Zinsou", "IM", "passager", None),
]


class Command(BaseCommand):
    help = "Loads demo data (idempotent: deletes the previous demo data first)."

    @transaction.atomic
    def handle(self, *args, **opts):
        User.objects.filter(username__in=[m[0] for m in MEMBRES]).delete()
        u = {}
        for username, prenom, nom, filiere, role, vehicule in MEMBRES:
            u[username] = User.objects.create_user(
                username=username, email=f"{username}@ifri-demo.bj", password=PASSWORD, first_name=prenom,
                last_name=nom, filiere=filiere, role=role, telephone="+229 01 00 00 00",
                bio=f"Étudiant(e) en {filiere} à l'IFRI.")
            if vehicule:
                Vehicule.objects.create(proprietaire=u[username], marque=vehicule[0], modele=vehicule[1],
                                        couleur=vehicule[2], places=vehicule[3])
        now = timezone.localtime().replace(minute=0, second=0, microsecond=0)

        def trajet(cond, a, b, jours, heure, places, prix, desc=""):
            la, lb = LIEUX[a], LIEUX[b]
            return Trajet.objects.create(
                conducteur=u[cond], lieu_depart=la[0], lat_depart=la[1], lng_depart=la[2], lieu_arrivee=lb[0],
                lat_arrivee=lb[1], lng_arrivee=lb[2], places_total=places, prix=prix, description=desc,
                date_depart=(now + timedelta(days=jours)).replace(hour=heure, minute=30 if heure % 2 else 0))

        t1 = trajet("koffi", "godomey", "IFRI", 1, 7, 3, 300, "Départ devant la station Total. Je passe par Zogbadjè.")
        t2 = trajet("rita", "etoile", "IFRI", 1, 6, 3, 500, "Clim, ponctuelle. Merci d'être à l'heure.")
        t3 = trajet("marc", "kpota", "IFRI", 1, 7, 1, 200, "Moto, casque fourni.")
        trajet("koffi", "IFRI", "godomey", 1, 17, 3, 300, "Retour après les cours.")
        trajet("rita", "akpakpa", "IFRI", 2, 6, 3, 600)
        trajet("koffi", "fidjrosse", "IFRI", 3, 7, 3, 500)
        trajet("marc", "togba", "IFRI", 2, 8, 1, 200)
        trajet("rita", "IFRI", "cadjehoun", 2, 18, 3, 500, "Je peux déposer à Vèdoko.")

        services.accepter(services.reserver(t1, u["awa"], 1, "Je serai à la station."), u["koffi"])
        services.reserver(t1, u["jean"], 1, "Bonjour, il reste une place ?")
        services.accepter(services.reserver(t3, u["ella"], 1), u["marc"])
        services.reserver(t2, u["awa"], 1)

        # a past ride with reviews
        passe = trajet("koffi", "godomey", "IFRI", 10, 7, 3, 300)
        for p in ("awa", "ella"):
            Reservation.objects.create(trajet=passe, passager=u[p], places=1, statut=Reservation.Statut.CONFIRMEE)
        Trajet.objects.filter(pk=passe.pk).update(date_depart=now - timedelta(days=4))
        Avis.objects.create(auteur=u["awa"], cible=u["koffi"], trajet=passe, note=5, commentaire="Très ponctuel, conduite prudente.")
        Avis.objects.create(auteur=u["ella"], cible=u["koffi"], trajet=passe, note=4, commentaire="Bonne ambiance, un peu de retard au départ.")
        Avis.objects.create(auteur=u["koffi"], cible=u["awa"], trajet=passe, note=5, commentaire="Passagère au rendez-vous à l'heure.")

        conv = conversation_entre(u["awa"], u["koffi"], t1)
        for auteur, texte in [("awa", "Bonjour Koffi, je serai à la station Total vers 7h20."),
                              ("koffi", "Parfait, je pars à 7h30 pile. Voiture grise."),
                              ("awa", "Super, merci !")]:
            Message.objects.create(conversation=conv, auteur=u[auteur], contenu=texte, lu=auteur == "awa")
        self.stdout.write(self.style.SUCCESS(
            f"Demo data loaded: {len(MEMBRES)} members, {Trajet.objects.count()} rides. Password: {PASSWORD}"))
