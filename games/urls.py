from django.urls import path, include
from . import views

urlpatterns = [
  path("game/<int:game_id>", views.game, name="game"),
  path("", views.browse, name="home"),
]