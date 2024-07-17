from django.db import connection, DatabaseError
from django.core.management import call_command
from django.db import migrations
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
    
    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self, log_entry: dict):
        self.log_entry = log_entry

    def rotate_logs(self):
        """
            (rotate_logs): This method will rotate the log entries by removing them if and only if the log entry is behind 30 minutes. It will also remove duplicated entries 
                Params: 
                    self: an object that is apart of the constructor.
        """
        current_time = datetime.now()
        for timestamp_str in list(self.log_entry.keys()):
            timestamp = datetime.fromisoformat(timestamp_str)
            hours_diff = (current_time - timestamp).total_seconds() / 60
            if hours_diff >= 1:
                del self.log_entry[timestamp_str]

    def create_logging_table(self):
        """
            (create_logging_table): This method will create a relational database called TicTackToe_logging
            Params:
                self: an object that is apart of the constructor.
        """
        try:
            table_exists = 'logging' in connection.introspection.table_names()
            if not table_exists:
                call_command('makemigrations', 'TicTackToe')
                call_command('migrate')
                with connection.schema_editor() as schema_editor:
                    schema_editor.create_model(Logging)
                text = "Logging table created successfully."
                self.log_entry[datetime.now().isoformat()] = text
        except DatabaseError as e:
            text = f"Error creating Logging table: {e}"
            self.log_entry[datetime.now().isoformat()] = text

    def get_queryset(self):
        """
            (get_queryset): This method is a getter method. It queries all the entities and the attributes and stores them into a dictionary 
            Params:
                self: An object that is apart of the constructor which allows type mangling 
        """
        return Logging.objects.all()

    
logging_init = LoggingViewSet({}) # Create a constant instance

class GameViewSet(viewsets.ModelViewSet):
    '''
        This class represents a singleton static class.
    '''
    _instance = None  # Class variable to hold the singleton instance

    @staticmethod
    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super().__new__(cls)
        return cls._instance

    
    @staticmethod 
    def create_game_table():
        """
            (create_game_table): This method creates a relational database table called TicTackToe_game if it does not exist
            Params:
                None
            Returns:
                None
        """
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
            logging_init.log_entry[datetime.now().isoformat()] = f"Error creating game table: {e}"


    @staticmethod
    def get_queryset():
        """
            (get_queryset): This method is a getter method. It queries all the entities and the attributes and stores them into a dictionary 
            Params:
                self: An object that is apart of the constructor which allows type mangling 
        """

        return Game.objects.all()

    
    
class WinnerViewSet(viewsets.ModelViewSet):
    '''
        This class has methods that can create the Game table, Query from it, and obtain the serial
    '''


    _instance = None  # Class variable to hold the singleton instance

    @staticmethod
    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super().__new__(cls)
        return cls._instance


    @staticmethod 
    def create_winner_table():
        """
            (create_winner_table): This method creates a relational database table called TicTackToe_winner if it does not exist
            Params:
                None
            Returns:
                None
        """
        try:
            # Ensuring the winner table exists
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
    def get_queryset():
        """
            (get_queryset): This method is a getter method. It queries all the entities and the attributes and stores them into a dictionary 
            Params:
                self: An object that is apart of the constructor which allows type mangling 
        """
        return Winner.objects.all()
    
    

@api_view(['GET', 'POST'])
def start_game(request):
    """
        A Djagno api end point that shows the game has been started followed by the id
    """
    history = {}
    try:
        GameViewSet.create_game_table()
        if not Game.objects.exists():
            history["Game History"] = {}
            Game.objects.create(history=history, current_move=0)
            Game.objects.create(game_id='001')
        data = request.data
        match request.method:
            case 'POST':
                if data is None:
                    return Response({"Game History": "No history data provided."}, status=status.HTTP_400_BAD_REQUEST)
                else:
                    game = Game.objects.get(game_id='001')
                    history["Game History"] = data
                    game.history = history # This should avoid duplicated entries 
                    game.current_move = 0
                    game.save() 
            case 'GET':
                try:    
                    data = GameViewSet.get_queryset
                    serializer = GameSerializer(data, context={'request': request}, many=True)
                    GameViewSet.set_serialize = serializer
                except Exception as e:
                    logging_init.log_entry[datetime.now().isoformat()] = f'from start_game {e}'
        game = Game.objects.get(game_id='001')
        # Serialize the game instance
        serializer = GameSerializer(game)
        return Response({"Game History": serializer.data}, status=status.HTTP_200_OK)
    except Exception as e:
        # Handle any exceptions that occur during game creation
        logging_init.log_entry[datetime.now().isoformat()] = f"Error starting game: {e}"
        return Response({"Game History": serializer.data}, status=status.HTTP_200_OK)
    
@api_view(['GET','POST'])
def logging(request):
    """
        Logs the game events. Must launch it manually by issuing http://localhost:8000/polls/logging

        Parameters:
        - request: The HTTP request containing data to be logged.
    """
    try:
        logging_init.create_logging_table()
        if not Logging.objects.exists():
            Logging.objects.create(logging_id='003')
            Logging.objects.create(entries={})
        data = request.data
        match request.method:
            case 'POST':
                if data is None:
                    print("Something Happend!")
                logging_init.log_entry.update(dict(data))
                log = Logging.objects.get(logging_id='003')
                log.entries.update(logging_init.log_entry)
                log.save()
            case 'GET':
                # GET method is probably needed because if the developer refreshes the page, it will keep it up to date
                try:
                    serializer = LoggingSerializer(data=request.data)
                    if serializer.is_valid():
                        serializer.save()
                except Exception as e:
                    # Update the database to hold new data
                    logging_init.log_entry[datetime.now().isoformat()] = f'from  logging function: {e}'
        logging_init.rotate_logs() # Rotate the logs
        log = Logging.objects.get(logging_id='003')
        serializer = LoggingSerializer(log)
        return Response({"Log Entries": serializer.data}, status=status.HTTP_200_OK)
    except Exception as e:
        # Handle any exceptions that occur during game creation
        logging_init.log_entry[datetime.now().isoformat()] = f"Error starting game: {e}"
        return Response({"Log Entries": logging_init.log_entry}, status=status.HTTP_200_OK)


@api_view(['GET','POST'])
def winner(request):
    """
        Represents who won. Will launch once there is a winner

        Parameters:
        - request: The HTTP request containing data
    """
    try:
        WinnerViewSet.create_winner_table()
        if not Winner.objects.exists():
            Winner.objects.create(winner_id='002')
            Winner.objects.create(amount_of_times={})
        data = request.data
        match request.method:
            case 'POST':
                if data is None:
                    # Add a return statement here after merging everything in main: July 16th, 2024
                    print("Something happend in the winner funciton")
                _winner = Winner.objects.get(winner_id='002')
                _winner.amount_of_times.update(request.data)
                _winner.save()
            case 'GET':
                try:
                    serializer = WinnerSerializer(data=request.data)
                    if serializer.is_valid():
                        serializer.save()
                except Exception as e:
                    logging_init.log_entry[datetime.now().isoformat()] = f'from winner.html file POST method: {e}'
        _winner = Winner.objects.get(winner_id='002')
        serializer = WinnerSerializer(_winner) # always serialize your data as it won't work if you tried displaying it in the Django's api
        return Response({"Winner Board": serializer.data}, status=status.HTTP_200_OK)
    except Exception as e:
        # Handle any exceptions that occur during game creation
        logging_init.log_entry[datetime.now().isoformat()] = f"Error starting game: {e}"
        return Response({"Log Entries": logging_init.log_entry}, status=status.HTTP_200_OK)
