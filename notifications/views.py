from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST


@login_required
def liste(request):
    return render(request, "notifications/liste.html",
                  {"notifications": request.user.notifications.all()[:50]})


@login_required
def ouvrir(request, pk):
    n = get_object_or_404(request.user.notifications, pk=pk)
    n.lue = True
    n.save(update_fields=["lue"])
    return redirect(n.lien or "notifications:liste")


@login_required
@require_POST
def tout_lire(request):
    request.user.notifications.filter(lue=False).update(lue=True)
    return redirect("notifications:liste")


@login_required
def api_compteur(request):
    return JsonResponse({"non_lues": request.user.notifications.filter(lue=False).count()})
