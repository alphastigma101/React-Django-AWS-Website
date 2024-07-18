from rest_framework import serializers
from .models import Game, Logging, Winner


class GameSerializer(serializers.ModelSerializer):
    '''
        A class that represents serialization for the Game model. 
        Use this class to serialize the data and send it to Django's api end point 
    '''
    class Meta:
        '''
            A class that stores metadata about the GameSerializer class
        '''
        model = Game
        fields = ['game_id', 'history']


class LoggingSerializer(serializers.ModelSerializer):
    '''
        A class that represents serialization for the Logging model
    '''
    class Meta:
        '''
            A class that stores metadata about the LoggingSerializer class
        '''
        model = Logging
        fields = ['logging_id', 'entries']



class WinnerSerializer(serializers.ModelSerializer):
    '''
        A class that represents serialization for the Winner model
    '''
    class Meta:
        '''
            A class that stores metadata about the LoggingSerializer class
        '''
        model = Winner
        fields = ['winner_id', 'amount_of_times']

