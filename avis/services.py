from .models import Avis


def participants(trajet):
    return [trajet.conducteur, *trajet.passagers_confirmes()]


def peut_noter(trajet, auteur, cible):
    if not trajet.est_passe or trajet.statut == trajet.Statut.ANNULE:
        return False, "Vous pourrez laisser un avis après le trajet."
    gens = participants(trajet)
    if auteur not in gens or cible not in gens:
        return False, "Seuls les participants du trajet peuvent laisser un avis."
    if auteur == cible:
        return False, "Vous ne pouvez pas vous noter vous-même."
    if trajet.conducteur != auteur and trajet.conducteur != cible:
        return False, "Les avis se font entre le conducteur et ses passagers."
    if Avis.objects.filter(auteur=auteur, cible=cible, trajet=trajet).exists():
        return False, "Vous avez déjà laissé un avis."
    return True, ""


def personnes_a_noter(trajet, user):
    """Participants the user can still rate for this ride."""
    if not user.is_authenticated:
        return []
    return [p for p in participants(trajet) if peut_noter(trajet, user, p)[0]]
