from datetime import timedelta

from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from core.testing import conducteur, membre, trajet
from notifications.models import Notification

from . import services
from .models import Reservation, Trajet


class ReservationRulesTest(TestCase):
    def setUp(self):
        self.koffi = conducteur()
        self.awa = membre("awa")
        self.jean = membre("jean")
        self.t = trajet(self.koffi, places=2)

    def test_full_booking_cycle_and_notifications(self):
        r = services.reserver(self.t, self.awa, 1, "Je serai au carrefour")
        self.assertEqual(r.statut, Reservation.Statut.EN_ATTENTE)
        self.assertTrue(Notification.objects.filter(destinataire=self.koffi, type="reservation").exists())
        services.accepter(r, self.koffi)
        self.assertEqual(self.t.places_restantes, 1)
        self.assertTrue(Notification.objects.filter(destinataire=self.awa, type="acceptee").exists())

    def test_trip_becomes_full_then_reopens_on_cancel(self):
        r1 = services.reserver(self.t, self.awa, 1)
        r2 = services.reserver(self.t, self.jean, 1)
        services.accepter(r1, self.koffi)
        services.accepter(r2, self.koffi)
        self.t.refresh_from_db()
        self.assertEqual(self.t.statut, Trajet.Statut.COMPLET)
        services.annuler_reservation(r2, self.jean)
        self.t.refresh_from_db()
        self.assertEqual(self.t.statut, Trajet.Statut.OUVERT)
        self.assertEqual(self.t.places_restantes, 1)

    def test_cannot_book_own_trip(self):
        with self.assertRaises(services.ReservationError):
            services.reserver(self.t, self.koffi, 1)

    def test_cannot_book_more_seats_than_available(self):
        with self.assertRaises(services.ReservationError):
            services.reserver(self.t, self.awa, 3)

    def test_cannot_book_past_or_cancelled_trip(self):
        passe = trajet(self.koffi, dans_heures=-2)
        with self.assertRaises(services.ReservationError):
            services.reserver(passe, self.awa, 1)
        services.annuler_trajet(self.t, self.koffi)
        with self.assertRaises(services.ReservationError):
            services.reserver(self.t, self.awa, 1)

    def test_no_double_booking_but_rebook_after_refusal(self):
        r = services.reserver(self.t, self.awa, 1)
        with self.assertRaises(services.ReservationError):
            services.reserver(self.t, self.awa, 1)
        services.refuser(r, self.koffi)
        r2 = services.reserver(self.t, self.awa, 1)
        self.assertEqual(r2.pk, r.pk)
        self.assertEqual(r2.statut, Reservation.Statut.EN_ATTENTE)

    def test_only_driver_can_accept_and_not_twice(self):
        r = services.reserver(self.t, self.awa, 1)
        with self.assertRaises(services.ReservationError):
            services.accepter(r, self.jean)
        services.accepter(r, self.koffi)
        with self.assertRaises(services.ReservationError):
            services.accepter(r, self.koffi)

    def test_accept_rejected_when_seats_were_taken_meanwhile(self):
        r1 = services.reserver(self.t, self.awa, 2)
        r2 = services.reserver(self.t, self.jean, 1)
        services.accepter(r1, self.koffi)
        with self.assertRaises(services.ReservationError):
            services.accepter(r2, self.koffi)

    def test_cancelling_trip_cancels_reservations_and_notifies(self):
        r = services.reserver(self.t, self.awa, 1)
        services.accepter(r, self.koffi)
        services.annuler_trajet(self.t, self.koffi)
        r.refresh_from_db()
        self.assertEqual(r.statut, Reservation.Statut.ANNULEE)
        self.assertTrue(Notification.objects.filter(destinataire=self.awa, type="annulation").exists())


class LocalTimeTest(TestCase):
    def test_title_uses_benin_local_time(self):
        t = trajet(conducteur())
        local = timezone.localtime(t.date_depart)
        self.assertIn(f"{local:%H:%M}", str(t))


class SearchViewTest(TestCase):
    def setUp(self):
        self.koffi = conducteur()
        trajet(self.koffi, lieu_depart="Godomey")
        trajet(self.koffi, lieu_depart="Calavi Kpota")
        trajet(self.koffi, lieu_depart="Cotonou Akpakpa", dans_heures=-5)   # past: hidden

    def test_search_filters_and_hides_past_trips(self):
        r = self.client.get(reverse("trajets:recherche"))
        self.assertEqual(r.context["page"].paginator.count, 2)
        r = self.client.get(reverse("trajets:recherche"), {"depart": "godo"})
        self.assertEqual(r.context["page"].paginator.count, 1)

    def test_search_by_date(self):
        demain = (timezone.localtime() + timedelta(hours=24)).date()
        r = self.client.get(reverse("trajets:recherche"), {"date": demain.isoformat()})
        self.assertEqual(r.context["page"].paginator.count, 2)


class BookingViewTest(TestCase):
    def test_booking_through_the_web(self):
        koffi, awa = conducteur(), membre("awa")
        t = trajet(koffi)
        self.client.force_login(awa)
        r = self.client.post(reverse("trajets:reserver", args=[t.pk]), {"places": 2, "message": "merci"})
        self.assertRedirects(r, t.get_absolute_url())
        resa = Reservation.objects.get()
        self.client.force_login(koffi)
        self.client.post(reverse("trajets:accepter", args=[resa.pk]))
        resa.refresh_from_db()
        self.assertEqual(resa.statut, Reservation.Statut.CONFIRMEE)

    def test_booking_requires_login(self):
        t = trajet(conducteur())
        r = self.client.post(reverse("trajets:reserver", args=[t.pk]), {"places": 1})
        self.assertIn(reverse("login:connexion"), r.url)
