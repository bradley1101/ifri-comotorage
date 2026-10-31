from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.views import LoginView, LogoutView
from django.shortcuts import redirect, render

from .forms import ConnexionForm, InscriptionForm


class Connexion(LoginView):
    template_name = "login/connexion.html"
    authentication_form = ConnexionForm
    redirect_authenticated_user = True


class Deconnexion(LogoutView):
    pass


def inscription(request):
    if request.user.is_authenticated:
        return redirect("dashboard:index")
    form = InscriptionForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        user = form.save()
        login(request, user)
        messages.success(request, f"Bienvenue sur IFRI Comotorage, {user.first_name} !")
        return redirect("profil:vehicule" if user.peut_conduire else "dashboard:index")
    return render(request, "login/inscription.html", {"form": form})
