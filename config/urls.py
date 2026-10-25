from django.contrib import admin
from django.urls import include, path

from polls.views import home


urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("accounts.urls")),
    path("", include("polls.urls")),
    path("", home, name="home"),
]
