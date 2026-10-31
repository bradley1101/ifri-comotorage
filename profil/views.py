from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone

from avis.models import Avis
from trajets.models import Trajet
from users.models import User

from .forms import ProfilForm, VehiculeForm
from .models import Vehicule


@login_required
def mon_profil(request):
    return redirect("profil:public", username=request.user.username)


def public(request, username):
    membre = get_object_or_404(User, username=username)
    return render(request, "profil/public.html", {
        "membre": membre,
        "vehicule": Vehicule.objects.filter(proprietaire=membre).first(),
        "resume": Avis.resume(membre),
        "avis": Avis.objects.filter(cible=membre).select_related("auteur", "trajet")[:10],
        "trajets": Trajet.objects.filter(conducteur=membre, statut=Trajet.Statut.OUVERT,
                                         date_depart__gt=timezone.now())[:5],
        "nb_trajets": Trajet.objects.filter(conducteur=membre).exclude(statut=Trajet.Statut.ANNULE).count(),
    })


@login_required
def modifier(request):
    form = ProfilForm(request.POST or None, instance=request.user)
    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Profil mis à jour.")
        return redirect("profil:moi")
    return render(request, "profil/form.html", {"form": form, "titre": "Modifier mon profil"})


@login_required
def vehicule(request):
    instance = Vehicule.objects.filter(proprietaire=request.user).first()
    form = VehiculeForm(request.POST or None, instance=instance)
    if request.method == "POST" and form.is_valid():
        v = form.save(commit=False)
        v.proprietaire = request.user
        v.save()
        messages.success(request, "Véhicule enregistré. Vous pouvez publier un trajet.")
        return redirect("publication_offre:nouvelle")
    return render(request, "profil/form.html", {"form": form, "titre": "Mon véhicule"})
