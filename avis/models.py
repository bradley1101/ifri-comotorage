from django.conf import settings
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.db.models import Avg, Count


class Avis(models.Model):
    """Rating left after a ride, by a driver or a passenger, about another participant."""

    auteur = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="avis_donnes")
    cible = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="avis_recus")
    trajet = models.ForeignKey("trajets.Trajet", on_delete=models.CASCADE, related_name="avis")
    note = models.PositiveSmallIntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    commentaire = models.TextField(blank=True, max_length=500)
    cree_le = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "avis"
        ordering = ["-cree_le"]
        constraints = [
            models.UniqueConstraint(fields=["auteur", "cible", "trajet"], name="un_avis_par_personne_et_trajet"),
            models.CheckConstraint(condition=models.Q(note__gte=1, note__lte=5), name="note_entre_1_et_5"),
        ]

    def __str__(self):
        return f"{self.auteur} → {self.cible} : {self.note}/5"

    @staticmethod
    def resume(user):
        r = Avis.objects.filter(cible=user).aggregate(moyenne=Avg("note"), nombre=Count("id"))
        return {"moyenne": round(r["moyenne"], 1) if r["moyenne"] else None, "nombre": r["nombre"]}
