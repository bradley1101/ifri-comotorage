from django.conf import settings
from django.db import models


class Notification(models.Model):
    class Type(models.TextChoices):
        RESERVATION = "reservation", "Nouvelle demande de réservation"
        ACCEPTEE = "acceptee", "Réservation acceptée"
        REFUSEE = "refusee", "Réservation refusée"
        ANNULATION = "annulation", "Annulation"
        MESSAGE = "message", "Nouveau message"
        AVIS = "avis", "Nouvel avis"

    destinataire = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="notifications")
    type = models.CharField(max_length=12, choices=Type.choices)
    texte = models.CharField(max_length=255)
    lien = models.CharField(max_length=255, blank=True)
    lue = models.BooleanField(default=False)
    cree_le = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-cree_le"]

    def __str__(self):
        return f"{self.destinataire}: {self.texte}"
