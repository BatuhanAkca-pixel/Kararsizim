from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.views import LoginView, LogoutView
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.utils.http import url_has_allowed_host_and_scheme

from .forms import RegisterForm, TurkishAuthenticationForm


def _safe_next_url(request):
    candidate = request.POST.get("next") or request.GET.get("next")
    if candidate and url_has_allowed_host_and_scheme(
        candidate,
        allowed_hosts={request.get_host()},
        require_https=request.is_secure(),
    ):
        return candidate
    return None


def register(request):
    if request.user.is_authenticated:
        return redirect("home")

    form = RegisterForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        user = form.save()
        login(request, user)
        messages.success(request, "Hesabın hazır. Hoş geldin!")
        return redirect(_safe_next_url(request) or "home")

    return render(
        request,
        "accounts/register.html",
        {"form": form, "next": _safe_next_url(request)},
    )


class AccountLoginView(LoginView):
    template_name = "accounts/login.html"
    authentication_form = TurkishAuthenticationForm
    redirect_authenticated_user = True

    def form_valid(self, form):
        messages.success(self.request, "Giriş yaptın. Hoş geldin!")
        return super().form_valid(form)


class AccountLogoutView(LogoutView):
    next_page = reverse_lazy("home")

    def post(self, request, *args, **kwargs):
        messages.success(request, "Güvenli şekilde çıkış yaptın.")
        return super().post(request, *args, **kwargs)
