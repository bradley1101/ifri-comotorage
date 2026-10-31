from django.conf import settings
from django.core.validators import MinValueValidator
from django.db import models
from django.db.models import Sum
from django.urls import reverse
from django.utils import timezone


class Trajet(models.Model):
    """A ride offered by a driver."""

    class Statut(models.TextChoices):
        OUVERT = "ouvert", "Ouvert"
        COMPLET = "complet", "Complet"
        ANNULE = "annule", "Annulé"

    conducteur = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="trajets")
    lieu_depart = models.CharField("lieu de départ", max_length=120)
    lat_depart = models.DecimalField(max_digits=9, decimal_places=6)
    lng_depart = models.DecimalField(max_digits=9, decimal_places=6)
    lieu_arrivee = models.CharField("lieu d'arrivée", max_length=120)
    lat_arrivee = models.DecimalField(max_digits=9, decimal_places=6)
    lng_arrivee = models.DecimalField(max_digits=9, decimal_places=6)
    date_depart = models.DateTimeField("date et heure de départ")
    places_total = models.PositiveSmallIntegerField("places proposées", validators=[MinValueValidator(1)])
    prix = models.PositiveIntegerField("prix par place (FCFA)", default=0)
    description = models.TextField(blank=True, max_length=600)
    bagages = models.BooleanField("bagages acceptés", default=True)
    statut = models.CharField(max_length=8, choices=Statut.choices, default=Statut.OUVERT)
    cree_le = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["date_depart"]
        indexes = [models.Index(fields=["statut", "date_depart"])]

    def __str__(self):
        return f"{self.lieu_depart} → {self.lieu_arrivee} ({timezone.localtime(self.date_depart):%d/%m %H:%M})"

    def get_absolute_url(self):
        return reverse("trajets:detail", args=[self.pk])

    @property
    def places_reservees(self):
        return self.reservations.filter(statut=Reservation.Statut.CONFIRMEE).aggregate(
            n=Sum("places"))["n"] or 0

    @property
    def places_restantes(self):
        return max(0, self.places_total - self.places_reservees)

    @property
    def est_passe(self):
        return self.date_depart <= timezone.now()

    @property
    def reservable(self):
        return self.statut == self.Statut.OUVERT and not self.est_passe and self.places_restantes > 0

    def passagers_confirmes(self):
        return [r.passager for r in self.reservations.filter(statut=Reservation.Statut.CONFIRMEE)
                .select_related("passager")]


class Reservation(models.Model):
    class Statut(models.TextChoices):
        EN_ATTENTE = "en_attente", "En attente"
        CONFIRMEE = "confirmee", "Confirmée"
        REFUSEE = "refusee", "Refusée"
        ANNULEE = "annulee", "Annulée"

    trajet = models.ForeignKey(Trajet, on_delete=models.CASCADE, related_name="reservations")
    passager = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="reservations")
    places = models.PositiveSmallIntegerField(default=1, validators=[MinValueValidator(1)])
    message = models.CharField(max_length=300, blank=True)
    statut = models.CharField(max_length=10, choices=Statut.choices, default=Statut.EN_ATTENTE)
    cree_le = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-cree_le"]
        constraints = [models.UniqueConstraint(fields=["trajet", "passager"], name="une_reservation_par_trajet")]

    def __str__(self):
        return f"{self.passager} · {self.trajet} · {self.get_statut_display()}"

    @property
    def active(self):
        return self.statut in (self.Statut.EN_ATTENTE, self.Statut.CONFIRMEE)
