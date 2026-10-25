from django.urls import path

from . import views


app_name = "polls"

urlpatterns = [
    path("anket/olustur/", views.create_poll, name="create"),
    path("anketlerim/", views.my_polls, name="mine"),
    path("anket/<uuid:poll_id>/", views.poll_detail, name="detail"),
    path("anket/<uuid:poll_id>/oy-ver/", views.vote, name="vote"),
]
