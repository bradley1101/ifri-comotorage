"""Booking rules. Views call these functions; they raise ReservationError on a rule violation."""
from django.db import transaction
from django.utils import timezone

from notifications.models import Notification
from notifications.services import notifier

from .models import Reservation, Trajet


class ReservationError(Exception):
    pass


@transaction.atomic
def reserver(trajet: Trajet, passager, places: int, message: str = "") -> Reservation:
    trajet = Trajet.objects.select_for_update().get(pk=trajet.pk)
    if trajet.conducteur_id == passager.id:
        raise ReservationError("Vous ne pouvez pas réserver votre propre trajet.")
    if not trajet.reservable:
        raise ReservationError("Ce trajet n'est plus disponible.")
    if places < 1 or places > trajet.places_restantes:
        raise ReservationError(f"Il reste {trajet.places_restantes} place(s) sur ce trajet.")

    existing = Reservation.objects.filter(trajet=trajet, passager=passager).first()
    if existing and existing.active:
        raise ReservationError("Vous avez déjà une réservation sur ce trajet.")
    if existing:  # previously refused / cancelled: a new request reuses the row
        existing.places, existing.message, existing.statut = places, message, Reservation.Statut.EN_ATTENTE
        existing.save()
        resa = existing
    else:
        resa = Reservation.objects.create(trajet=trajet, passager=passager, places=places, message=message)

    notifier(trajet.conducteur, Notification.Type.RESERVATION,
             f"{passager.nom_affiche} demande {places} place(s) pour {trajet.lieu_depart} → {trajet.lieu_arrivee}.",
             trajet.get_absolute_url())
    return resa


@transaction.atomic
def accepter(resa: Reservation, conducteur) -> Reservation:
    trajet = Trajet.objects.select_for_update().get(pk=resa.trajet_id)
    if trajet.conducteur_id != conducteur.id:
        raise ReservationError("Seul le conducteur peut accepter une réservation.")
    if resa.statut != Reservation.Statut.EN_ATTENTE:
        raise ReservationError("Cette demande a déjà été traitée.")
    if resa.places > trajet.places_restantes:
        raise ReservationError("Il n'y a plus assez de places pour accepter cette demande.")
    resa.statut = Reservation.Statut.CONFIRMEE
    resa.save(update_fields=["statut"])
    if trajet.places_restantes == 0:
        trajet.statut = Trajet.Statut.COMPLET
        trajet.save(update_fields=["statut"])
    notifier(resa.passager, Notification.Type.ACCEPTEE,
             f"{conducteur.nom_affiche} a accepté votre réservation pour {trajet.lieu_depart} → {trajet.lieu_arrivee}.",
             trajet.get_absolute_url())
    return resa


def refuser(resa: Reservation, conducteur) -> Reservation:
    if resa.trajet.conducteur_id != conducteur.id:
        raise ReservationError("Seul le conducteur peut refuser une réservation.")
    if resa.statut != Reservation.Statut.EN_ATTENTE:
        raise ReservationError("Cette demande a déjà été traitée.")
    resa.statut = Reservation.Statut.REFUSEE
    resa.save(update_fields=["statut"])
    notifier(resa.passager, Notification.Type.REFUSEE,
             f"Votre demande pour {resa.trajet.lieu_depart} → {resa.trajet.lieu_arrivee} a été refusée.",
             resa.trajet.get_absolute_url())
    return resa


@transaction.atomic
def annuler_reservation(resa: Reservation, passager) -> Reservation:
    if resa.passager_id != passager.id:
        raise ReservationError("Vous ne pouvez annuler que vos propres réservations.")
    if not resa.active:
        raise ReservationError("Cette réservation n'est plus active.")
    trajet = Trajet.objects.select_for_update().get(pk=resa.trajet_id)   # fresh state, locked
    if trajet.est_passe:
        raise ReservationError("Le trajet a déjà eu lieu.")
    etait_confirmee = resa.statut == Reservation.Statut.CONFIRMEE
    resa.statut = Reservation.Statut.ANNULEE
    resa.save(update_fields=["statut"])
    if etait_confirmee and trajet.statut == Trajet.Statut.COMPLET:
        trajet.statut = Trajet.Statut.OUVERT          # a seat is free again
        trajet.save(update_fields=["statut"])
    notifier(trajet.conducteur, Notification.Type.ANNULATION,
             f"{passager.nom_affiche} a annulé sa réservation ({trajet.lieu_depart} → {trajet.lieu_arrivee}).",
             trajet.get_absolute_url())
    return resa


@transaction.atomic
def annuler_trajet(trajet: Trajet, conducteur) -> Trajet:
    trajet = Trajet.objects.select_for_update().get(pk=trajet.pk)
    if trajet.conducteur_id != conducteur.id:
        raise ReservationError("Seul le conducteur peut annuler ce trajet.")
    if trajet.statut == Trajet.Statut.ANNULE:
        raise ReservationError("Ce trajet est déjà annulé.")
    trajet.statut = Trajet.Statut.ANNULE
    trajet.save(update_fields=["statut"])
    for resa in trajet.reservations.filter(statut__in=[Reservation.Statut.EN_ATTENTE, Reservation.Statut.CONFIRMEE]):
        resa.statut = Reservation.Statut.ANNULEE
        resa.save(update_fields=["statut"])
        notifier(resa.passager, Notification.Type.ANNULATION,
                 f"Le trajet {trajet.lieu_depart} → {trajet.lieu_arrivee} du {timezone.localtime(trajet.date_depart):%d/%m} a été annulé.",
                 trajet.get_absolute_url())
    return trajet
