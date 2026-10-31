"""Shared helpers for the test suites."""
from datetime import timedelta

from django.utils import timezone

from profil.models import Vehicule
from trajets.models import Trajet
from users.models import User


def membre(username, role=User.Role.PASSAGER, **kw):
    return User.objects.create_user(username=username, email=f"{username}@ifri.uac.bj", password="motdepasse-123",
                                    first_name=username.capitalize(), role=role, **kw)


def conducteur(username="koffi"):
    u = membre(username, role=User.Role.CONDUCTEUR)
    Vehicule.objects.create(proprietaire=u, marque="Toyota", modele="Corolla", couleur="grise", places=4)
    return u


def trajet(conducteur, dans_heures=24, places=3, **kw):
    data = dict(lieu_depart="Godomey", lat_depart=6.385, lng_depart=2.345, lieu_arrivee="IFRI",
                lat_arrivee=6.418, lng_arrivee=2.342, date_depart=timezone.now() + timedelta(hours=dans_heures),
                places_total=places, prix=500)
    data.update(kw)
    return Trajet.objects.create(conducteur=conducteur, **data)
