from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render

from notifications.models import Notification
from notifications.services import notifier
from trajets.models import Trajet
from users.models import User

from .forms import AvisForm
from .services import peut_noter


@login_required
def noter(request, trajet_pk, username):
    trajet = get_object_or_404(Trajet, pk=trajet_pk)
    cible = get_object_or_404(User, username=username)
    ok, raison = peut_noter(trajet, request.user, cible)
    if not ok:
        messages.error(request, raison)
        return redirect(trajet)
    form = AvisForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        avis = form.save(commit=False)
        avis.auteur, avis.cible, avis.trajet = request.user, cible, trajet
        avis.save()
        notifier(cible, Notification.Type.AVIS, f"{request.user.nom_affiche} vous a laissé un avis ({avis.note}/5).",
                 f"/profil/{cible.username}/")
        messages.success(request, "Merci pour votre avis !")
        return redirect(trajet)
    return render(request, "avis/form.html", {"form": form, "trajet": trajet, "cible": cible})
