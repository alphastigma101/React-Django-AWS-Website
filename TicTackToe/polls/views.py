from django.db import connection, DatabaseError
from django.core.management import call_command
from django.db import migrations
import json
from .models import Game, Logging, Winner
from .serializers import GameSerializer, LoggingSerializer, WinnerSerializer
from rest_framework import viewsets, status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from datetime import datetime


class LoggingViewSet(viewsets.ViewSet):
    '''
        A class that implements the singleton method and also represents the the logging view
    '''
    _instance = None  # Class variable to hold the singleton instance
    __serialize = None
    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self, log_entry: dict):
        self.log_entry = log_entry

    def rotate_logs(self):
        current_time = datetime.now()
        for timestamp_str in list(self.log_entry.keys()):
            timestamp = datetime.fromisoformat(timestamp_str)
            hours_diff = (current_time - timestamp).total_seconds() / 3600
            if hours_diff >= 3:
                del self.log_entry[timestamp_str]

    def create_logging_table(self):
        try:
            table_exists = 'logging' in connection.introspection.table_names()
            if not table_exists:
                call_command('makemigrations', 'TicTackToe')
                call_command('migrate')
                with connection.schema_editor() as schema_editor:
                    schema_editor.create_model(Logging)
                text = "Game table created successfully."
                self.log_entry[datetime.now().isoformat()] = text
        except DatabaseError as e:
            text = f"Error creating game table: {e}"
            self.log_entry[datetime.now().isoformat()] = text

    def get_queryset(self):
        return Logging.objects.all()

    def set_serialize(self, serialize):
        self.__serialize = serialize

    def get_serialize(self):
        return self.__serialize

logging_init = LoggingViewSet({}) # Create a constant instance

class GameViewSet(viewsets.ModelViewSet):
    '''
        This class has methods that can create the Game table, Query from it, and obtain the serial
    '''
    __serialize = None

    @staticmethod 
    def create_game_table():
        try:
            # Ensure the game_game table exists
            table_exists = 'game' in connection.introspection.table_names()
            
            if not table_exists:
                # Run migrations to ensure the database schema is up to date
                call_command('makemigrations', 'TicTackToe')
                call_command('migrate')
                
                # Create the Game model table
                with connection.schema_editor() as schema_editor:
                    schema_editor.create_model(Game)
                logging_init.log_entry[datetime.now().isoformat()] = "Game table created successfully."
        except DatabaseError as e:
            # Handle database errors
            logging_init.log_entry[datetime.now().isoformat()] = f"Error creating game table: {e}"

    @staticmethod
    def get_queryset():
        return Game.objects.all()

    @staticmethod
    def  get_serialize():
        return GameViewSet.__serialize

    @staticmethod
    def get_serialize():
        return GameViewSet.__serialize


class WinnerViewSet(viewsets.ModelViewSet):
    '''
        This class has methods that can create the Game table, Query from it, and obtain the serial
    '''
    __serialize = None

    @staticmethod 
    def create_winner_table():
        try:
            # Ensure the game_game table exists
            table_exists = 'winner' in connection.introspection.table_names()
            
            if not table_exists:
                # Run migrations to ensure the database schema is up to date
                call_command('makemigrations', 'TicTackToe')
                call_command('migrate')
                
                # Create the Game model table
                with connection.schema_editor() as schema_editor:
                    schema_editor.create_model(Winner)
                logging_init.log_entry[datetime.now().isoformat()] = "Winner Table has been created"

        except DatabaseError as e:
            # Handle database errors
            text = f'Error creating Winner table: {e}'
            logging_init.log_entry[datetime.now().isoformat()] = text
    
    @staticmethod
    def set_serialize(serialize):
        WinnerViewSet.__serialize = serialize

    @staticmethod
    def get_serialize():
        return WinnerViewSet.__serialize

    @staticmethod
    def get_queryset():
        return Winner.objects.all()


@api_view(['GET'])
def start_game(request):
    """
        An Djagno api end point that shows the game has been started followed by the id
    """
    try:
        start_game_data = request.query_params.get('history', None)
        if start_game_data is None:
            return Response({"Game History": "No history data provided."}, status=status.HTTP_400_BAD_REQUEST)
        # Parse the data into Json format 
        start_game_data = json.loads(start_game_data)
        GameViewSet.create_game_table()
        if not Game.objects.exists():
            Game.objects.create(history=start_game_data, current_move=0)
            Game.objects.create(game_id='001')
        else:
            game = Game.objects.get(game_id='001')
            game.history.update(request.data)
            game.current_move = 0
            game.save() 
        match request.method:
            case 'GET':
                try:
                    data = GameViewSet.get_queryset
                    serializer = GameSerializer(data, context={'request': request}, many=True)
                    GameViewSet.set_serialize = serializer
                except Exception as e:
                    logging_init.log_entry[datetime.now().isoformat()] = f'from start_game {e}'
        return Response({"Game History": request.data}, status=status.HTTP_200_OK)
    except Exception as e:
        # Handle any exceptions that occur during game creation
        logging_init.log_entry[datetime.now().isoformat()] = f"Error starting game: {e}"
        return Response({"Game History": request.data}, status=status.HTTP_200_OK)
    
@api_view(['GET'])
def logging(request):
    """
        Logs the game events. Must launch it manually by issuing http://localhost:8000/polls/logging

        Parameters:
        - request: The HTTP request containing data to be logged.
    """
    try:
        logging_game_data = request.data.get('logs', {})  # Retrieve the JSON data sent in the request
        if (len(logging_game_data) > 0):
             logging_init.log_entry.update(request.data)
        logging_init.create_logging_table()
        # Create a new game instance
        if not Logging.objects.exists():
            Logging.objects.create(logging_id='001')
            Logging.objects.create(entries=request.data.get('log_history', {}))
        else:
            log = Logging.objects.get(logging_id='001')
            log.entries.update(request.data)
            log.save()
        match request.method:
            case 'GET':
                try:
                    logging_init.rotate_logs()
                    serializer = LoggingSerializer(data=request.data)
                    logging_init.set_serialize(serializer)
                    if serializer.is_valid():
                        serializer.save()
                except Exception as e:
                    # Update the database to hold new data
                    logging_init.log_entry[datetime.now().isoformat()] = f'from  logging function: {e}'
        return Response({"Log Entries": logging_init.log_entry}, status=status.HTTP_200_OK)
    except Exception as e:
        # Handle any exceptions that occur during game creation
        logging_init.log_entry[datetime.now().isoformat()] = f"Error starting game: {e}"
        return Response({"Log Entries": logging_init.log_entry}, status=status.HTTP_200_OK)


@api_view(['GET'])
def winner(request):
    """
        Represents who won. Will launch once there is a winner

        Parameters:
        - request: The HTTP request containing data
    """
    try:
        winner_game_data = request.data.get('winner_history', {})  # Retrieve the JSON data sent in the request
        # Ensure the game table is created if not already
        WinnerViewSet.create_winner_table()
        WinnerViewSet.create_winner_table()
        # Create a new game instance
        if not Winner.objects.exists():
            Winner.objects.create(winner_id='001')
            Winner.objects.create(amount_of_times=winner_game_data.get('winner_history', {}))
        else:
            _winner = Winner.objects.get(winner_id='001')
            _winner.amount_of_times.update(request.data)
            _winner.save()
        match request.method:
            case 'GET':
                try:
                    serializer = WinnerSerializer(data=request.data)
                    WinnerViewSet.set_serialize = serializer
                    if serializer.is_valid():
                        serializer.save()
                except Exception as e:
                    logging_init.log_entry[datetime.now().isoformat()] = f'from winner.html file POST method: {e}'
        data = WinnerViewSet.get_queryset()
        serializer = WinnerSerializer(data, context={'request': request}, many=True)
        WinnerViewSet.set_serialize = serializer
        return Response({"Winner Board": request.data}, status=status.HTTP_200_OK)
    except Exception as e:
        # Handle any exceptions that occur during game creation
        logging_init.log_entry[datetime.now().isoformat()] = f"Error starting game: {e}"
        return Response({"Log Entries": logging_init.log_entry}, status=status.HTTP_200_OK)
