from django import forms

from core.forms import StyledFormMixin

from .models import Avis


class AvisForm(StyledFormMixin, forms.ModelForm):
    note = forms.TypedChoiceField(choices=[(i, f"{i} ★") for i in range(5, 0, -1)], coerce=int,
                                  widget=forms.RadioSelect(attrs={"class": "stars"}))

    class Meta:
        model = Avis
        fields = ("note", "commentaire")
        widgets = {"commentaire": forms.Textarea(attrs={"rows": 3, "placeholder": "Ponctualité, conduite, ambiance…"})}
