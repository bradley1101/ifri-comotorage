from django import forms

from core.forms import StyledFormMixin

from .models import Reservation


class RechercheForm(StyledFormMixin, forms.Form):
    depart = forms.CharField(label="Départ", required=False,
                             widget=forms.TextInput(attrs={"placeholder": "ex. Godomey"}))
    arrivee = forms.CharField(label="Arrivée", required=False,
                              widget=forms.TextInput(attrs={"placeholder": "ex. IFRI"}))
    date = forms.DateField(label="Date", required=False, widget=forms.DateInput(attrs={"type": "date"}))
    places = forms.IntegerField(label="Places", required=False, min_value=1, max_value=8, initial=1)


class ReservationForm(StyledFormMixin, forms.ModelForm):
    class Meta:
        model = Reservation
        fields = ("places", "message")
        widgets = {"message": forms.TextInput(attrs={"placeholder": "Un mot pour le conducteur (facultatif)"})}
