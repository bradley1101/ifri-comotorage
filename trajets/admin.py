from django.contrib import admin

from .models import Reservation, Trajet


class ReservationInline(admin.TabularInline):
    model = Reservation
    extra = 0


@admin.register(Trajet)
class TrajetAdmin(admin.ModelAdmin):
    list_display = ("__str__", "conducteur", "places_total", "prix", "statut")
    list_filter = ("statut",)
    search_fields = ("lieu_depart", "lieu_arrivee", "conducteur__username")
    inlines = [ReservationInline]


@admin.register(Reservation)
class ReservationAdmin(admin.ModelAdmin):
    list_display = ("trajet", "passager", "places", "statut", "cree_le")
    list_filter = ("statut",)
