from django.test import TestCase
from django.urls import reverse

from users.models import User


class InscriptionTest(TestCase):
    def data(self, **kw):
        d = {"username": "awa", "first_name": "Awa", "last_name": "Sossa", "email": "awa@ifri.uac.bj",
             "telephone": "+22901000000", "filiere": "SEIOT", "role": "passager",
             "password1": "Covoit-IFRI-2025", "password2": "Covoit-IFRI-2025"}
        d.update(kw)
        return d

    def test_signup_logs_in(self):
        r = self.client.post(reverse("login:inscription"), self.data())
        self.assertRedirects(r, reverse("dashboard:index"))
        self.assertTrue(User.objects.filter(username="awa").exists())

    def test_driver_is_sent_to_vehicle_form(self):
        r = self.client.post(reverse("login:inscription"), self.data(role="conducteur"))
        self.assertRedirects(r, reverse("profil:vehicule"))

    def test_duplicate_email_refused(self):
        self.client.post(reverse("login:inscription"), self.data())
        self.client.logout()
        r = self.client.post(reverse("login:inscription"), self.data(username="awa2", email="AWA@ifri.uac.bj"))
        self.assertEqual(r.status_code, 200)
        self.assertEqual(User.objects.count(), 1)
