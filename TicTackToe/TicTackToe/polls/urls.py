from django.urls import path
from .views import GameViewSet, start_game, LoggingViewSet, logging, WinnerViewSet, winner


urlpatterns = [
    path("start_game", start_game, name="start_game"),
    path("logging", logging, name="start_game"),
    path("winner", winner, name="start_game"),
]
