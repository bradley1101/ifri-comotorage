from django.contrib.auth.decorators import login_required
from django.db.models import Sum
from django.shortcuts import render
from django.utils import timezone

from avis.models import Avis
from avis.services import personnes_a_noter
from trajets.models import Reservation, Trajet


@login_required
def index(request):
    u, now = request.user, timezone.now()
    mes_trajets = (Trajet.objects.filter(conducteur=u, date_depart__gt=now)
                   .exclude(statut=Trajet.Statut.ANNULE).prefetch_related("reservations"))
    demandes = (Reservation.objects.filter(trajet__conducteur=u, statut=Reservation.Statut.EN_ATTENTE,
                                           trajet__date_depart__gt=now).select_related("passager", "trajet"))
    mes_reservations = (Reservation.objects.filter(passager=u, trajet__date_depart__gt=now)
                        .exclude(statut=Reservation.Statut.ANNULEE).select_related("trajet", "trajet__conducteur"))
    passes = (Trajet.objects.filter(date_depart__lte=now).exclude(statut=Trajet.Statut.ANNULE)
              .filter(conducteur=u) | Trajet.objects.filter(
                  date_depart__lte=now, reservations__passager=u,
                  reservations__statut=Reservation.Statut.CONFIRMEE)).distinct().order_by("-date_depart")[:10]
    a_noter = [(t, p) for t in passes for p in personnes_a_noter(t, u)]
    stats = {
        "trajets_proposes": Trajet.objects.filter(conducteur=u).exclude(statut=Trajet.Statut.ANNULE).count(),
        "passagers_transportes": Reservation.objects.filter(
            trajet__conducteur=u, statut=Reservation.Statut.CONFIRMEE, trajet__date_depart__lte=now
        ).aggregate(n=Sum("places"))["n"] or 0,
        "trajets_passager": Reservation.objects.filter(passager=u, statut=Reservation.Statut.CONFIRMEE).count(),
        "note": Avis.resume(u),
    }
    return render(request, "dashboard/index.html", {
        "mes_trajets": mes_trajets, "demandes": demandes, "mes_reservations": mes_reservations,
        "a_noter": a_noter, "stats": stats})
