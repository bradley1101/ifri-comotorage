from django.conf import settings
from django.db import models
from django.urls import reverse


class Conversation(models.Model):
    participants = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name="conversations")
    trajet = models.ForeignKey("trajets.Trajet", on_delete=models.SET_NULL, null=True, blank=True,
                               related_name="conversations")
    mis_a_jour = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-mis_a_jour"]

    def __str__(self):
        return " / ".join(str(u) for u in self.participants.all())

    def get_absolute_url(self):
        return reverse("messaging:conversation", args=[self.pk])

    def autre(self, user):
        return self.participants.exclude(pk=user.pk).first()

    def non_lus(self, user):
        return self.messages.filter(lu=False).exclude(auteur=user).count()


class Message(models.Model):
    conversation = models.ForeignKey(Conversation, on_delete=models.CASCADE, related_name="messages")
    auteur = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="messages_envoyes")
    contenu = models.TextField(max_length=1000)
    envoye_le = models.DateTimeField(auto_now_add=True)
    lu = models.BooleanField(default=False)

    class Meta:
        ordering = ["envoye_le", "id"]

    def __str__(self):
        return f"{self.auteur}: {self.contenu[:40]}"

    def as_dict(self, viewer):
        return {"id": self.id, "auteur": self.auteur.nom_affiche, "moi": self.auteur_id == viewer.id,
                "contenu": self.contenu, "heure": self.envoye_le.isoformat()}
