from django.db import models

class Game(models.Model):
    '''
        A class that represents entities for the ticktacktoe_game table
    '''
    game_id = models.CharField(max_length=4, primary_key=True)
    history = models.JSONField(default=dict)
    current_move = models.IntegerField(default=0)
    class Meta:
        '''
            A class the represents metadata about the Game class
            Note: 
                app_label: app_label and another string are concated together based on this delimeter: _ 
                    Ex: ticktacktoe_game <- This will be the database table name that stores the entities history and current move
        '''
        app_label = 'ticktacktoe'

class Winner(models.Model):
    '''
        A class that represents entities for ticktacktoe_winner table
    '''
    #game_id = models.ForeignKey(Game, on_delete=models.CASCADE) # References the pks inside the Game Table
    winner_id = models.CharField(max_length=4, primary_key=True)
    amount_of_times = models.JSONField(default=dict)

    class Meta:
        app_label = 'ticktacktoe'

class Logging(models.Model):
    '''
        A class that is a model that holds entities for the ticktacktoe_logging table
    '''
    logging_id = models.CharField(max_length=4, primary_key=True)
    #winner_id = models.ForeignKey(Winner, on_delete=models.CASCADE) # References the pks inside the winner table
    entries = models.JSONField(default=dict)
    class Meta:
        app_label = 'ticktacktoe'

