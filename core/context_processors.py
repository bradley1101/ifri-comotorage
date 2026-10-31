from django.conf import settings


def compteurs(request):
    """Unread notifications / messages for the navigation bar, and map defaults."""
    data = {"IFRI_LAT": settings.IFRI_LAT, "IFRI_LNG": settings.IFRI_LNG}
    user = getattr(request, "user", None)
    if user and user.is_authenticated:
        from messaging.models import Message
        data["nb_notifications"] = user.notifications.filter(lue=False).count()
        data["nb_messages"] = (Message.objects.filter(conversation__participants=user, lu=False)
                               .exclude(auteur=user).count())
    return data
