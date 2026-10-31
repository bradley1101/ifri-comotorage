from .models import Notification


def notifier(destinataire, type_, texte, lien=""):
    """Single entry point used by the other apps to notify a user."""
    return Notification.objects.create(destinataire=destinataire, type=type_, texte=texte, lien=lien)
