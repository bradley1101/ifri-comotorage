"""Instant messaging between members (JSON polling every few seconds, no extra server needed)."""
from django.contrib.auth.decorators import login_required
from django.db.models import Count
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST

from notifications.models import Notification
from notifications.services import notifier
from trajets.models import Trajet
from users.models import User

from .models import Conversation, Message


def conversation_entre(u1, u2, trajet=None):
    # annotate BEFORE filtering on participants, otherwise the joins inflate the count
    conv = (Conversation.objects.annotate(n=Count("participants")).filter(n=2)
            .filter(participants=u1).filter(participants=u2).first())
    if conv is None:
        conv = Conversation.objects.create(trajet=trajet)
        conv.participants.add(u1, u2)
    elif trajet and conv.trajet_id != trajet.id:
        conv.trajet = trajet
        conv.save(update_fields=["trajet"])
    return conv


@login_required
def boite(request):
    convs = request.user.conversations.prefetch_related("participants").select_related("trajet")
    items = [{"conv": c, "autre": c.autre(request.user), "dernier": c.messages.last(),
              "non_lus": c.non_lus(request.user)} for c in convs]
    return render(request, "messaging/boite.html", {"items": items})


@login_required
def demarrer(request, username):
    autre = get_object_or_404(User, username=username)
    if autre == request.user:
        return redirect("messaging:boite")
    trajet = Trajet.objects.filter(pk=request.GET.get("trajet")).first() if request.GET.get("trajet") else None
    return redirect(conversation_entre(request.user, autre, trajet))


@login_required
def conversation(request, pk):
    conv = get_object_or_404(Conversation, pk=pk, participants=request.user)
    conv.messages.exclude(auteur=request.user).update(lu=True)
    msgs = conv.messages.select_related("auteur")
    return render(request, "messaging/conversation.html", {
        "conv": conv, "autre": conv.autre(request.user), "messages_conv": msgs,
        "dernier_id": msgs.last().id if msgs else 0})


@login_required
def api_messages(request, pk):
    conv = get_object_or_404(Conversation, pk=pk, participants=request.user)
    after = int(request.GET.get("after", 0) or 0)
    nouveaux = list(conv.messages.filter(id__gt=after).select_related("auteur"))
    conv.messages.filter(id__gt=after).exclude(auteur=request.user).update(lu=True)
    return JsonResponse({"messages": [m.as_dict(request.user) for m in nouveaux]})


@login_required
@require_POST
def api_envoyer(request, pk):
    conv = get_object_or_404(Conversation, pk=pk, participants=request.user)
    contenu = (request.POST.get("contenu") or "").strip()[:1000]
    if not contenu:
        return JsonResponse({"error": "Message vide"}, status=400)
    msg = Message.objects.create(conversation=conv, auteur=request.user, contenu=contenu)
    conv.save(update_fields=["mis_a_jour"])
    autre = conv.autre(request.user)
    # one notification per burst: only if the previous unread notification was read
    if autre and not autre.notifications.filter(type=Notification.Type.MESSAGE, lue=False,
                                                lien=conv.get_absolute_url()).exists():
        notifier(autre, Notification.Type.MESSAGE, f"Nouveau message de {request.user.nom_affiche}",
                 conv.get_absolute_url())
    return JsonResponse({"message": msg.as_dict(request.user)})
