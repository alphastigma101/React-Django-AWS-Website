from django.urls import path
from .views import GameViewSet, start_game, LoggingViewSet, logging, WinnerViewSet, winner


urlpatterns = [
    path("start_game", start_game),
    path("logging", logging),
    path("winner", winner),
]
