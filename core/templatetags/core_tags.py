from django import template
from django.contrib.humanize.templatetags.humanize import intcomma

register = template.Library()


@register.filter
def fcfa(value):
    """12500 -> '12 500 FCFA', 0 -> 'Gratuit'."""
    try:
        value = int(value)
    except (TypeError, ValueError):
        return value
    return "Gratuit" if value == 0 else f"{intcomma(value).replace(',', ' ')} FCFA"


@register.filter
def etoiles(note):
    """4.3 -> '★★★★☆'."""
    if note is None:
        return ""
    n = int(round(float(note)))
    return "★" * n + "☆" * (5 - n)


@register.inclusion_tag("core/avatar.html")
def avatar(user, size=40):
    palette = ["#1e6f5c", "#c2410c", "#4338ca", "#a16207", "#be185d", "#0e7490"]
    return {"u": user, "size": size, "color": palette[user.pk % len(palette)] if user.pk else palette[0]}
