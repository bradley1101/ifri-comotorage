from django.test import TestCase
from django.urls import reverse

from core.testing import conducteur, membre

from .models import Conversation


class MessagingTest(TestCase):
    def setUp(self):
        self.koffi, self.awa, self.jean = conducteur(), membre("awa"), membre("jean")

    def test_conversation_send_poll_and_read(self):
        self.client.force_login(self.awa)
        r = self.client.get(reverse("messaging:demarrer", args=["koffi"]))
        conv = Conversation.objects.get()
        self.assertRedirects(r, conv.get_absolute_url())
        # same pair -> same conversation
        self.client.get(reverse("messaging:demarrer", args=["koffi"]))
        self.assertEqual(Conversation.objects.count(), 1)

        r = self.client.post(reverse("messaging:api_envoyer", args=[conv.pk]), {"contenu": "Bonjour !"})
        first_id = r.json()["message"]["id"]
        self.assertEqual(self.koffi.notifications.filter(type="message").count(), 1)
        self.client.post(reverse("messaging:api_envoyer", args=[conv.pk]), {"contenu": "Vous passez par Godomey ?"})
        self.assertEqual(self.koffi.notifications.filter(type="message").count(), 1)   # no spam

        self.client.force_login(self.koffi)
        data = self.client.get(reverse("messaging:api_messages", args=[conv.pk]), {"after": first_id}).json()
        self.assertEqual([m["contenu"] for m in data["messages"]], ["Vous passez par Godomey ?"])
        self.assertEqual(conv.non_lus(self.koffi), 1)          # only fetched messages are marked read
        self.client.get(conv.get_absolute_url())               # opening the conversation reads everything
        self.assertEqual(conv.non_lus(self.koffi), 0)

    def test_outsider_cannot_read(self):
        self.client.force_login(self.awa)
        self.client.get(reverse("messaging:demarrer", args=["koffi"]))
        conv = Conversation.objects.get()
        self.client.force_login(self.jean)
        self.assertEqual(self.client.get(reverse("messaging:api_messages", args=[conv.pk])).status_code, 404)

    def test_empty_message_rejected(self):
        self.client.force_login(self.awa)
        self.client.get(reverse("messaging:demarrer", args=["koffi"]))
        conv = Conversation.objects.get()
        self.assertEqual(self.client.post(reverse("messaging:api_envoyer", args=[conv.pk]), {"contenu": "  "}).status_code, 400)
