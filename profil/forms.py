from django import forms

from core.forms import StyledFormMixin
from users.models import User

from .models import Vehicule


class ProfilForm(StyledFormMixin, forms.ModelForm):
    class Meta:
        model = User
        fields = ("first_name", "last_name", "email", "telephone", "filiere", "role", "bio")
        labels = {"first_name": "Prénom", "last_name": "Nom", "role": "Rôle", "bio": "Présentation"}
        widgets = {"bio": forms.Textarea(attrs={"rows": 3})}


class VehiculeForm(StyledFormMixin, forms.ModelForm):
    class Meta:
        model = Vehicule
        fields = ("marque", "modele", "couleur", "places", "immatriculation")
