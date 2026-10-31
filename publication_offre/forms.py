from django import forms
from django.utils import timezone

from core.forms import StyledFormMixin
from trajets.models import Trajet


class TrajetForm(StyledFormMixin, forms.ModelForm):
    class Meta:
        model = Trajet
        fields = ("lieu_depart", "lat_depart", "lng_depart", "lieu_arrivee", "lat_arrivee", "lng_arrivee",
                  "date_depart", "places_total", "prix", "bagages", "description")
        widgets = {
            "lat_depart": forms.HiddenInput(), "lng_depart": forms.HiddenInput(),
            "lat_arrivee": forms.HiddenInput(), "lng_arrivee": forms.HiddenInput(),
            "date_depart": forms.DateTimeInput(attrs={"type": "datetime-local"}, format="%Y-%m-%dT%H:%M"),
            "description": forms.Textarea(attrs={"rows": 3, "placeholder":
                                                 "Point de rendez-vous précis, arrêts possibles, horaires…"}),
            "lieu_depart": forms.TextInput(attrs={"placeholder": "ex. Carrefour Godomey"}),
            "lieu_arrivee": forms.TextInput(attrs={"placeholder": "ex. IFRI — UAC Abomey-Calavi"}),
        }

    def __init__(self, *args, vehicule=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.vehicule = vehicule
        if vehicule and not self.instance.pk:
            self.fields["places_total"].initial = vehicule.places
        for name in ("lat_depart", "lng_depart", "lat_arrivee", "lng_arrivee"):
            self.fields[name].error_messages["required"] = "Placez les deux points sur la carte."

    def clean_date_depart(self):
        d = self.cleaned_data["date_depart"]
        if d <= timezone.now():
            raise forms.ValidationError("Le départ doit être dans le futur.")
        return d

    def clean_places_total(self):
        n = self.cleaned_data["places_total"]
        if self.vehicule and n > self.vehicule.places:
            raise forms.ValidationError(f"Votre véhicule ne compte que {self.vehicule.places} place(s) passager.")
        if self.instance.pk and n < self.instance.places_reservees:
            raise forms.ValidationError(f"{self.instance.places_reservees} place(s) sont déjà réservées.")
        return n
