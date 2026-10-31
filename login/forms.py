from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm

from core.forms import StyledFormMixin
from users.models import User


class InscriptionForm(StyledFormMixin, UserCreationForm):
    class Meta:
        model = User
        fields = ("username", "first_name", "last_name", "email", "telephone", "filiere", "role")
        labels = {"username": "Nom d'utilisateur", "first_name": "Prénom", "last_name": "Nom",
                  "role": "Je souhaite être"}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for name in ("first_name", "last_name", "email"):
            self.fields[name].required = True

    def clean_email(self):
        email = self.cleaned_data["email"].lower()
        if User.objects.filter(email__iexact=email).exists():
            raise forms.ValidationError("Un compte existe déjà avec cette adresse.")
        return email


class ConnexionForm(StyledFormMixin, AuthenticationForm):
    pass
