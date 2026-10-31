from datetime import timedelta

from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from core.testing import conducteur, membre, trajet
from trajets import services
from trajets.models import Trajet


def payload(**kw):
    d = {"lieu_depart": "Godomey", "lat_depart": "6.385", "lng_depart": "2.345", "lieu_arrivee": "IFRI",
         "lat_arrivee": "6.418", "lng_arrivee": "2.342", "places_total": 3, "prix": 500, "bagages": "on",
         "date_depart": (timezone.localtime() + timedelta(days=1)).strftime("%Y-%m-%dT%H:%M"), "description": ""}
    d.update(kw)
    return d


class PublicationTest(TestCase):
    def setUp(self):
        self.koffi = conducteur()
        self.client.force_login(self.koffi)

    def test_publish_trip(self):
        r = self.client.post(reverse("publication_offre:nouvelle"), payload())
        t = Trajet.objects.get()
        self.assertRedirects(r, t.get_absolute_url())
        self.assertEqual(t.conducteur, self.koffi)

    def test_requires_vehicle(self):
        self.client.force_login(membre("awa"))
        r = self.client.get(reverse("publication_offre:nouvelle"))
        self.assertRedirects(r, reverse("profil:vehicule"))

    def test_rejects_past_date_missing_map_points_and_too_many_seats(self):
        past = (timezone.localtime() - timedelta(hours=1)).strftime("%Y-%m-%dT%H:%M")
        for data in (payload(date_depart=past), payload(lat_depart=""), payload(places_total=9)):
            r = self.client.post(reverse("publication_offre:nouvelle"), data)
            self.assertEqual(r.status_code, 200)
        self.assertFalse(Trajet.objects.exists())

    def test_cannot_reduce_seats_below_confirmed(self):
        t = trajet(self.koffi, places=3)
        awa = membre("awa")
        services.accepter(services.reserver(t, awa, 2), self.koffi)
        r = self.client.post(reverse("publication_offre:modifier", args=[t.pk]), payload(places_total=1))
        self.assertEqual(r.status_code, 200)
        t.refresh_from_db()
        self.assertEqual(t.places_total, 3)

    def test_other_user_cannot_edit(self):
        t = trajet(self.koffi)
        self.client.force_login(membre("intrus"))
        self.assertEqual(self.client.get(reverse("publication_offre:modifier", args=[t.pk])).status_code, 404)
