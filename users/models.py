from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """IFRI student or staff member using the carpooling platform."""

    class Role(models.TextChoices):
        PASSAGER = "passager", "Passager"
        CONDUCTEUR = "conducteur", "Conducteur"
        LES_DEUX = "les_deux", "Conducteur et passager"

    class Filiere(models.TextChoices):
        SEIOT = "SEIOT", "Systèmes Embarqués et IoT"
        GL = "GL", "Génie Logiciel"
        IA = "IA", "Intelligence Artificielle"
        SI = "SI", "Sécurité Informatique"
        IM = "IM", "Internet et Multimédia"
        AUTRE = "AUTRE", "Personnel / autre"

    email = models.EmailField("adresse e-mail", unique=True)
    telephone = models.CharField("téléphone", max_length=20, blank=True)
    role = models.CharField(max_length=12, choices=Role.choices, default=Role.PASSAGER)
    filiere = models.CharField("filière", max_length=8, choices=Filiere.choices, default=Filiere.AUTRE)
    bio = models.TextField(blank=True, max_length=500)

    @property
    def initiales(self):
        nom = (self.first_name[:1] + self.last_name[:1]) or self.username[:2]
        return nom.upper()

    @property
    def nom_affiche(self):
        return self.get_full_name() or self.username

    @property
    def peut_conduire(self):
        return self.role in (self.Role.CONDUCTEUR, self.Role.LES_DEUX)

    def __str__(self):
        return self.nom_affiche
