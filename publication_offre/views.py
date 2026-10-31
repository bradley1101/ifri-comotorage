from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST

from profil.models import Vehicule
from trajets import services
from trajets.models import Trajet

from .forms import TrajetForm


@login_required
def nouvelle(request):
    vehicule = Vehicule.objects.filter(proprietaire=request.user).first()
    if vehicule is None:
        messages.info(request, "Enregistrez d'abord votre véhicule pour proposer un trajet.")
        return redirect("profil:vehicule")
    form = TrajetForm(request.POST or None, vehicule=vehicule)
    if request.method == "POST" and form.is_valid():
        trajet = form.save(commit=False)
        trajet.conducteur = request.user
        trajet.save()
        if not request.user.peut_conduire:
            request.user.role = request.user.Role.LES_DEUX
            request.user.save(update_fields=["role"])
        messages.success(request, "Votre trajet est publié.")
        return redirect(trajet)
    return render(request, "publication_offre/form.html", {"form": form, "titre": "Proposer un trajet"})


@login_required
def modifier(request, pk):
    trajet = get_object_or_404(Trajet, pk=pk, conducteur=request.user)
    if trajet.statut == Trajet.Statut.ANNULE or trajet.est_passe:
        messages.error(request, "Ce trajet ne peut plus être modifié.")
        return redirect(trajet)
    vehicule = Vehicule.objects.filter(proprietaire=request.user).first()
    form = TrajetForm(request.POST or None, instance=trajet, vehicule=vehicule)
    if request.method == "POST" and form.is_valid():
        trajet = form.save(commit=False)
        trajet.statut = Trajet.Statut.COMPLET if trajet.places_restantes == 0 else Trajet.Statut.OUVERT
        trajet.save()
        messages.success(request, "Trajet mis à jour.")
        return redirect(trajet)
    return render(request, "publication_offre/form.html", {"form": form, "titre": "Modifier le trajet", "trajet": trajet})


@login_required
@require_POST
def annuler(request, pk):
    trajet = get_object_or_404(Trajet, pk=pk)
    try:
        services.annuler_trajet(trajet, request.user)
        messages.success(request, "Trajet annulé. Les passagers ont été prévenus.")
    except services.ReservationError as e:
        messages.error(request, str(e))
    return redirect(trajet)
