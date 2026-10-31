from django.conf import settings
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models


class Vehicule(models.Model):
    proprietaire = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="vehicule")
    marque = models.CharField(max_length=40)
    modele = models.CharField("modèle", max_length=40)
    couleur = models.CharField(max_length=30)
    places = models.PositiveSmallIntegerField(
        "places passagers", validators=[MinValueValidator(1), MaxValueValidator(8)], default=3)
    immatriculation = models.CharField(max_length=15, blank=True)

    class Meta:
        verbose_name = "véhicule"

    def __str__(self):
        return f"{self.marque} {self.modele} ({self.couleur})"
