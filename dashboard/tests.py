from django.test import TestCase
from django.urls import reverse

from core.testing import conducteur, membre, trajet
from trajets import services


class PagesTest(TestCase):
    """Every page renders, for visitors and members."""

    def setUp(self):
        self.koffi, self.awa = conducteur(), membre("awa")
        self.t = trajet(self.koffi)
        services.reserver(self.t, self.awa, 1)

    def test_public_pages(self):
        for url in (reverse("accueil:index"), reverse("accueil:a_propos"), reverse("trajets:recherche"),
                    self.t.get_absolute_url(), reverse("profil:public", args=["koffi"]),
                    reverse("login:connexion"), reverse("login:inscription")):
            self.assertEqual(self.client.get(url).status_code, 200, url)

    def test_member_pages(self):
        for user in (self.koffi, self.awa):
            self.client.force_login(user)
            for url in (reverse("dashboard:index"), reverse("notifications:liste"), reverse("messaging:boite"),
                        reverse("profil:modifier"), reverse("profil:vehicule"), self.t.get_absolute_url()):
                self.assertEqual(self.client.get(url).status_code, 200, (user, url))

    def test_dashboard_shows_pending_request_to_driver(self):
        self.client.force_login(self.koffi)
        r = self.client.get(reverse("dashboard:index"))
        self.assertEqual(len(r.context["demandes"]), 1)

    def test_private_pages_require_login(self):
        r = self.client.get(reverse("dashboard:index"))
        self.assertEqual(r.status_code, 302)
