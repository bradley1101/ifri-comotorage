from datetime import datetime, time, timedelta

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone
from django.views.decorators.http import require_POST

from avis.services import personnes_a_noter

from . import services
from .forms import RechercheForm, ReservationForm
from .models import Reservation, Trajet


def recherche(request):
    form = RechercheForm(request.GET or None)
    qs = (Trajet.objects.filter(statut=Trajet.Statut.OUVERT, date_depart__gt=timezone.now())
          .select_related("conducteur"))
    if form.is_valid():
        d = form.cleaned_data
        if d["depart"]:
            qs = qs.filter(lieu_depart__icontains=d["depart"])
        if d["arrivee"]:
            qs = qs.filter(lieu_arrivee__icontains=d["arrivee"])
        if d["date"]:
            # range instead of __date: works on MySQL even without its time-zone tables
            debut = timezone.make_aware(datetime.combine(d["date"], time.min))
            qs = qs.filter(date_depart__gte=debut, date_depart__lt=debut + timedelta(days=1))
        if d["places"]:
            qs = [t for t in qs if t.places_restantes >= d["places"]]
    page = Paginator(list(qs), 10).get_page(request.GET.get("page"))
    return render(request, "trajets/recherche.html", {"form": form, "page": page})


def detail(request, pk):
    trajet = get_object_or_404(Trajet.objects.select_related("conducteur"), pk=pk)
    user = request.user
    ctx = {"trajet": trajet, "est_conducteur": user.is_authenticated and user.id == trajet.conducteur_id}
    if user.is_authenticated:
        ctx["ma_reservation"] = trajet.reservations.filter(passager=user).first()
        ctx["form"] = ReservationForm(initial={"places": 1})
        ctx["a_noter"] = personnes_a_noter(trajet, user)
    if ctx["est_conducteur"]:
        ctx["reservations"] = trajet.reservations.select_related("passager").order_by("statut", "cree_le")
    ctx["passagers"] = trajet.passagers_confirmes()
    return render(request, "trajets/detail.html", ctx)


@login_required
@require_POST
def reserver(request, pk):
    trajet = get_object_or_404(Trajet, pk=pk)
    form = ReservationForm(request.POST)
    if form.is_valid():
        try:
            services.reserver(trajet, request.user, form.cleaned_data["places"], form.cleaned_data["message"])
            messages.success(request, "Demande envoyée au conducteur. Vous serez notifié de sa réponse.")
        except services.ReservationError as e:
            messages.error(request, str(e))
    else:
        messages.error(request, "Formulaire invalide.")
    return redirect(trajet)


def _action(request, pk, fn, ok_message):
    resa = get_object_or_404(Reservation.objects.select_related("trajet", "passager"), pk=pk)
    try:
        fn(resa, request.user)
        messages.success(request, ok_message)
    except services.ReservationError as e:
        messages.error(request, str(e))
    return redirect(request.POST.get("next") or resa.trajet.get_absolute_url())


@login_required
@require_POST
def accepter(request, pk):
    return _action(request, pk, services.accepter, "Réservation acceptée.")


@login_required
@require_POST
def refuser(request, pk):
    return _action(request, pk, services.refuser, "Réservation refusée.")


@login_required
@require_POST
def annuler(request, pk):
    return _action(request, pk, services.annuler_reservation, "Réservation annulée.")
