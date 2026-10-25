from django.urls import path

from .views import AccountLoginView, AccountLogoutView, register


app_name = "accounts"

urlpatterns = [
    path("kayit-ol/", register, name="register"),
    path("giris-yap/", AccountLoginView.as_view(), name="login"),
    path("cikis-yap/", AccountLogoutView.as_view(), name="logout"),
]
