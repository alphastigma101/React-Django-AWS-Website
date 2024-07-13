from django.db import models

class Game(models.Model):
    history = models.JSONField(default=list)
    current_move = models.IntegerField(default=0)
    class Meta:
        app_label = 'ticktacktoe'

class Winner(models.Model):
    player = models.CharField(max_length=100)  # Assuming player names are stored as strings
    amount_of_times = models.IntegerField({'X': 0, 'O': 0})  # Assuming this tracks the number of wins

    class Meta:
        app_label = 'ticktacktoe'
