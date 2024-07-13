from django.urls import path
from .views import GameViewSet, start_game


urlpatterns = [
    path("start_game", start_game),
]
