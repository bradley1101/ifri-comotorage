from django.db.models import Sum
from django.shortcuts import render
from django.utils import timezone

from trajets.forms import RechercheForm
from trajets.models import Reservation, Trajet
from users.models import User


def index(request):
    prochains = (Trajet.objects.filter(statut=Trajet.Statut.OUVERT, date_depart__gt=timezone.now())
                 .select_related("conducteur")[:6])
    stats = {
        "membres": User.objects.filter(is_active=True).count(),
        "trajets": Trajet.objects.exclude(statut=Trajet.Statut.ANNULE).count(),
        "places": Reservation.objects.filter(statut=Reservation.Statut.CONFIRMEE).aggregate(n=Sum("places"))["n"] or 0,
    }
    points = [{"lat": float(t.lat_depart), "lng": float(t.lng_depart), "titre": str(t), "url": t.get_absolute_url()}
              for t in prochains]
    return render(request, "accueil/index.html",
                  {"form": RechercheForm(), "prochains": prochains, "stats": stats, "points": points})


def a_propos(request):
    return render(request, "accueil/a_propos.html")
