from django.test import TestCase
from django.urls import reverse

from core.testing import conducteur, membre, trajet
from trajets import services

from .models import Avis
from .services import peut_noter, personnes_a_noter


class AvisTest(TestCase):
    def setUp(self):
        self.koffi = conducteur()
        self.awa = membre("awa")
        self.jean = membre("jean")
        self.t = trajet(self.koffi, dans_heures=24)
        services.accepter(services.reserver(self.t, self.awa, 1), self.koffi)
        self.t.date_depart = self.t.date_depart.replace(year=self.t.date_depart.year - 1)   # trip is now past
        self.t.save()

    def test_participants_can_rate_each_other_once(self):
        self.assertEqual(personnes_a_noter(self.t, self.awa), [self.koffi])
        self.client.force_login(self.awa)
        self.client.post(reverse("avis:noter", args=[self.t.pk, "koffi"]), {"note": 5, "commentaire": "Ponctuel"})
        self.assertEqual(Avis.resume(self.koffi), {"moyenne": 5.0, "nombre": 1})
        self.assertFalse(peut_noter(self.t, self.awa, self.koffi)[0])

    def test_outsider_and_self_rating_refused(self):
        self.assertFalse(peut_noter(self.t, self.jean, self.koffi)[0])
        self.assertFalse(peut_noter(self.t, self.koffi, self.koffi)[0])

    def test_no_rating_before_the_trip(self):
        futur = trajet(self.koffi)
        services.accepter(services.reserver(futur, self.awa, 1), self.koffi)
        self.assertFalse(peut_noter(futur, self.awa, self.koffi)[0])
