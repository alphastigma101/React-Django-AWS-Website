from django.db import connection, DatabaseError # Catch any kind of error that occurs 
from django.core.management import call_command # Call in commands that update the server 
from django.db import migrations # Check and see if the models have been updated and populate the db 
from .models import Game, Logging, Winner # Import the models which are the database tables 
from .serializers import GameSerializer, LoggingSerializer, WinnerSerializer # import the serializer classes to serialize the data into json form
from rest_framework import viewsets, status # use status library to return a HTTP error code and use viewSets so it can be inherited from the singleton classes below
from rest_framework.decorators import api_view # Used for Django's api 
from rest_framework.response import Response # Use this if a exception occured
from datetime import datetime, timedelta # Import the datetime and timezone libraries for custom log entries
import traceback, inspect # Use this to print out the line where the exception occurred and the file it happened in
from .validation import Validation
current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")




class LoggingViewSet(viewsets.ViewSet, Validation):
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
        self.refreshed = {} # This method will check and see if the react app has refreshed itself or not

    def rotate_logs(self):
        """
            (rotate_logs): This method will rotate the log entries by removing them if and only if the log entry is behind 30 minutes. It will also remove duplicated entries 
                Params: 
                    self: an object that is apart of the constructor which allows access to public attributes.
        """
        for timestamp_str in list(self.log_entry.keys()):
            timestamp = datetime.fromisoformat(timestamp_str)
            # Convert the custom log entries into iso format so the diff can be found
            hours_diff = (datetime.fromisoformat(current_time) - timestamp).total_seconds() / 60
            if hours_diff >= 1:
                del self.log_entry[timestamp_str]
            #breakpoint()
            print("Checking to see if the logs will delete duplicated entries (Last)")
            values = tuple(self.log_entry.values()) # Make a tuple
            if (values.count(self.log_entry.get(timestamp_str)) > 1):
                # If there is more than the same value, remove it 
                del self.log_entry[timestamp_str]


    def create_logging_table(self):
        """
            (create_logging_table): This method will create a relational database called TicTackToe_logging
            Params:
            self: an object that is apart of the constructor which allows access to public attributes.
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
            frame = inspect.currentframe()                                         
            filename = frame.f_back.f_code.co_filename
            line_number = frame.f_back.f_lineno 
            funcname = frame.f_trace
            code = frame.f_code
            text = f"File: {filename}\n Line: {line_number}\n Function: {funcname}\n Code: {code}\n Error: {e}"
            self.log_entry[current_time] = text

    def get_queryset(self):
        """
            (get_queryset): This method is a getter method. It queries all the entities and the attributes and stores them into a dictionary 
            Params:
                self: an object that is apart of the constructor which allows access to public attributes.
        """
        return Logging.objects.all()

    
logging_init = LoggingViewSet({}) # Create a constant instance

class GameViewSet(viewsets.ModelViewSet,  Validation):
    '''
        This class represents a singleton static class.
    '''
    _instance = None  # Class variable to hold the singleton instance
    __new_game = 0
    __prev_game = 0

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
                logging_init.log_entry[curr_time] = "Game table created successfully."
        except DatabaseError as e:
            frame = inspect.currentframe()                                         
            filename = frame.f_back.f_code.co_filename
            line_number = frame.f_back.f_lineno 
            funcname = frame.f_trace
            code = frame.f_code
            logging_init.log_entry[current_time] = f"File: {filename}\n, Line: {line_number}\n, Function: {funcname}\n, Code: {code}\n"

    @staticmethod 
    def set_new_game(value:int) -> None:
        GameViewSet.__new_game += value

    
    @staticmethod
    def get_new_game(value:int) -> int:
        return int(GameViewSet.__new_game)

    @staticmethod
    def get_prev_game_value():
        return int(GameViewSet.__prev_game)
    
    @staticmethod
    def set_prev_game_value(value:int) -> None:
        GameViewSet.__prev_game += value

    @staticmethod
    def get_queryset():
        """
            (get_queryset): This method is a getter method. It queries all the entities and the attributes and stores them into a dictionary 
            Params:
                self: An object that is apart of the constructor which allows type mangling 
        """
        return Game.objects.all()

    
    
class WinnerViewSet(viewsets.ModelViewSet, Validation):
    '''
        This class has methods that can create the Game table, Query from it, and obtain the serial
    '''


    _instance = None  # Class variable to hold the singleton instance
    __new_board = 0
    __prev_board = 0

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
                logging_init.log_entry[current_time] = "Winner Table has been created"
        except DatabaseError as e:
            # Handle database errors
            frame = inspect.currentframe()                                         
            filename = frame.f_back.f_code.co_filename
            line_number = frame.f_back.f_lineno 
            funcname = frame.f_trace
            code = frame.f_code
            text = f"File: {filename}\n Line: {line_number}\n Function: {funcname}\n Code: {code}\n Error: {e}\n"
            logging_init.log_entry[current_time] = text
    
    @staticmethod 
    def set_new_score_board(value:int) -> None:
        WinnerViewSet.__new_board += value

    
    @staticmethod
    def get_new_score_board(value:int) -> int:
        return int(WinnerViewSet.__new_board)


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
    serializer = None
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
                    frame = inspect.currentframe()                                         
                    filename = frame.f_back.f_code.co_filename
                    line_number = frame.f_back.f_lineno 
                    funcname = frame.f_trace
                    code = frame.f_code
                    return Response({"Game History": f"File: {filename}\n Line: {line_number}\n Function: {funcname}\n Code: {code}\n Object is: {data}\n"}, status=status.HTTP_400_BAD_REQUEST)
                else:
                    game = Game.objects.get(game_id='001')
                    check = GameViewSet.validate_2d_array(data) # Validate the data without actually using the serialization.py modules 
                    try:
                        if (check is True):
                            # Check and see if the react app refreshed itself 
                            if (GameViewSet.get_new_game(None) > GameViewSet.get_prev_game_value()):
                                history[f"Game History {GameViewSet.get_new_game}"] = data
                                GameViewSet.set_prev_game(GameViewSet.get_new_game(None) + 1) # Increment it by one so this field won't get executed until the user refreshes the front end page
                                game.history[GameViewSet.get_new_game] = history # Add the new game that was started
                                game.current_move = 0
                                game.save() # Save the data
                            else:
                                game.history[GameViewSet.get_new_game].update(data) # Index into the correct dictionary field
                                game.current_move += 1 
                                game.save() 
                        else: 
                            ###
                            # Add more here such as logging and what not. July 17th 2024
                            text = "Data is not in the form of a two dimensional array!"
                    except Exception as e:
                        frame = inspect.currentframe()                                         
                        filename = frame.f_back.f_code.co_filename
                        line_number = frame.f_back.f_lineno 
                        funcname = frame.f_trace
                        code = frame.f_code
                        logging_init.log_entry[current_time] = f"File: {filename} \n Line: {line_number} \n Function: {funcname} \n Code: {code} \n Error: {e} \n" 
            case 'GET':
                try:
                    breakpoint()
                    print("Making sure that the data will be sent to the api (Second)")
                    game = Game.objects.get(game_id='001')
                    game.history.update(history)
                    serializer = GameSerializer(game) # serialize the data
                    game.history.update(history)
                    game.save()
                    return Response({"Game History": serializer.data}, status=status.HTTP_200_OK)
                except Exception as e:
                    frame = inspect.currentframe()                                         
                    filename = frame.f_back.f_code.co_filename
                    line_number = frame.f_back.f_lineno 
                    funcname = frame.f_trace
                    code = frame.f_code
                    logging_init.log_entry[current_time] = f"File: {filename} \n Line: {line_number} \n Function: {funcname} \n Code: {code} \n Error: {e} \n"
                    log = Logging.objects.get(logging_id='003')
                    serializer = LoggingSerializer(log)
                    return Response({"Log History": serializer.data}, status=status.HTTP_400_BAD_REQUEST)
        breakpoint()
        game = Game.objects.get(game_id='001')
        # Serialize the game instance
        serializer = GameSerializer(game)
        game.history.update(history)
        game.save()
        return Response({"Game History": serializer.data}, status=status.HTTP_200_OK)
    except Exception as e:
        # Handle any exceptions that occur during game creation
        frame = inspect.currentframe()                                         
        filename = frame.f_back.f_code.co_filename
        line_number = frame.f_back.f_lineno 
        funcname = frame.f_trace
        code = frame.f_code
        logging_init.log_entry[current_time] = f"File: {filename}\n Line: {line_number}\n Function: {funcname}\n Code: {code}\n Error: {e}\n"
        log = Logging.objects.get(logging_id='003') # Serialiing is needed because everything needs to be json serialized 
        serializer = LoggingSerializer(log)
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
                    frame = inspect.currentframe()                                         
                    filename = frame.f_back.f_code.co_filename
                    line_number = frame.f_back.f_lineno 
                    funcname = frame.f_trace
                    code = frame.f_code
                    return Response({"Log History": f"File: {filename}\n Line: {line_number}\n Function: {funcname}\n Code: {code}\n Object is: {data}\n"}, status=status.HTTP_400_BAD_REQUEST)
                check = logging_init.is_dictionary(data)
                if (check is True):
                    # Check to see if the data coming from react app is a dictionary 
                    if (len(logging_init.refreshed) <= 0):
                        # Store the timestamp of the game started
                        for key, value in data.items():
                            try:
                                timestamp = datetime.fromisoformat(key.replace("Z", "")) # Format it in isoformat
                                str_timestamp = timestamp.strftime("%Y-%m-%d %H:%M:%S")
                                key = str_timestamp
                                logging_init.refreshed[key] = value
                            except Exception as e:
                                frame = inspect.currentframe()                                         
                                filename = frame.f_back.f_code.co_filename
                                line_number = frame.f_back.f_lineno 
                                funcname = frame.f_trace
                                code = frame.f_code
                                logging_init.log_entry[timestamp] = f"Error parsing timestamp with fallback format: {e2}\nFile: {filename}\nLine: {line_number}\nFunction: {funcname}\nCode: {code}\n Error: {e}"
                    for key, value in logging_init.refreshed.items():
                        iso_conv = datetime.strptime(key, "%Y-%m-%d %H:%M:%S")
                        diff = (iso_conv - timestamp).total_seconds()
                        if (diff < 0):
                            # Game was refreshed 
                            GameViewSet.set_new_game(1)
                            GameViewSet.set_prev_game(1 - GameViewSet.get_new_game(None))
                        logging_init.log_entry[timestamp.strftime("%Y-%m-%d %H:%M:%S")] = value
                    ####
                    # Add more here later on July 17th, 2024
                    ####
                    #text = "data that was recieved is not a dictionary!"
            case 'GET':
                # GET method is needed because if the developer refreshes the page, it will keep it up to date
                try:
                    log = Logging.objects.get(logging_id='003')
                    logging_init.rotate_logs() # Rotate the logs if it is a GET request
                    log.entries.update(logging_init.log_entry)
                    serializer = LoggingSerializer(log) # serialize it
                    log.save()
                    return Response({"Log History": serializer.data}, status=status.HTTP_200_OK)
                except Exception as e:
                    # Update the database to hold new data
                    frame = inspect.currentframe()                                         
                    filename = frame.f_back.f_code.co_filename
                    line_number = frame.f_back.f_lineno 
                    funcname = frame.f_trace
                    code = frame.f_code
                    logging_init.log_entry[current_time] = f"File: {filename}\n Line: {line_number}\n Function: {funcname}\n Code: {code}\n Error: {e}\n"
                    log = Logging.objects.get(logging_id='003')
                    log.entries.update(logging_init.log_entry)
                    serializer = LoggingSerializer(log)
                    log.save()
                    return Response({"Log History": serializer.data}, status=status.HTTP_400_BAD_REQUEST)
        log = Logging.objects.get(logging_id='003')
        logging_init.rotate_logs() # Rotate the logs
        log.entries.update(logging_init.log_entry)
        serializer = LoggingSerializer(log)
        log.save()
        return Response({"Log History": serializer.data}, status=status.HTTP_200_OK)
    except Exception as e:
        # Handle any exceptions that occur during game creation
        frame = inspect.currentframe()                                         
        filename = frame.f_back.f_code.co_filename
        line_number = frame.f_back.f_lineno 
        funcname = frame.f_trace
        code = frame.f_code
        logging_init.log_entry[current_time] = f"File: {filename}\n Line: {line_number}\n Function: {funcname}\n Code: {code}\n Error: {e}\n"
        log = Logging.objects.get(logging_id='003') # Serialiing is needed because everything needs to be json serialized 
        log.entries.update(logging_init.log_entry)
        serializer = LoggingSerializer(log)
        log.save()
        return Response({"Log History": serializer.data}, status=status.HTTP_200_OK)



@api_view(['GET','POST'])
def winner(request):
    """
        Represents who won. Will launch once there is a winner

        Parameters:
        - request: The HTTP request containing data
    """
    history = {}
    try:
        WinnerViewSet.create_winner_table()
        if not Winner.objects.exists():
            Winner.objects.create(winner_id='002')
            Winner.objects.create(amount_of_times={})
        data = request.data
        match request.method:
            case 'POST':
                if data is None:
                    frame = inspect.currentframe()                                         
                    filename = frame.f_back.f_code.co_filename
                    line_number = frame.f_back.f_lineno 
                    funcname = frame.f_trace
                    code = frame.f_code
                check = WinnerViewSet.is_dictionary(data)
                if (check is True):
                    if (GameViewSet.get_new_game(None) > GameViewSet.get_prev_game()):
                        WinnerViewSet.set_new_score_board(WinnderViewSet.get_new_score_board(None) + 1)
                        # New game was started
                        history[f"Winner History {WinnerViewSet.get_score_board}"] = data
                        _winner = Winner.objects.get(winnner_id='002')
                        _winner.amount_of_times[WinnerViewSet.set_new_score_board] = history
                        _winner.save()
                    else:
                        _winner = Winner.objects.get(winner_id='002')
                        _winner.amount_of_times.update(request.data)
                        _winner.save()
                else:
                    ## 
                    # Add more here such as logging and what not July 17th 2024
                    text = "(winner): data is not in the form of a dictionary!"
                    ##
            case 'GET':
                try:
                    logging_init.rotate_logs()
                    _winner = Winner.objects.get(winner_id='002')
                    _winner.amount_of_times.update(data)
                    serializer = WinnerSerializer(_winner)
                    _winner.save()
                    return Response({"Winner Board": serializer.data}, status=status.HTTP_200_OK)
                except Exception as e:
                    frame = inspect.currentframe()                                         
                    filename = frame.f_back.f_code.co_filename
                    line_number = frame.f_back.f_lineno 
                    funcname = frame.f_trace
                    code = frame.f_code
                    logging_init.log_entry[current_time] = f"File: {filename}\n Line: {line_number}\n Function: {funcname}\n Code: {code}\n Error: {e}\n"
        _winner = Winner.objects.get(winner_id='002')
        _winner.amount_of_entries.update(data)
        serializer = WinnerSerializer(_winner) # always serialize your data as it won't work if you tried displaying it in the Django's api
        _winner.save()
        return Response({"Winner Board": serializer.data}, status=status.HTTP_200_OK)
    except Exception as e:
        # Handle any exceptions that occur during game creation
        frame = inspect.currentframe()                                         
        filename = frame.f_back.f_code.co_filename
        line_number = frame.f_back.f_lineno 
        funcname = frame.f_trace
        code = frame.f_code
        log = Logging.objects.get(logging_id='003') # Serialiing is needed because everything needs to be json serialized 
        serializer = LoggingSerializer(log)
        logging_init.log_entry[current_time] = f"File: {filename}\n Line: {line_number}\n Function: {funcname}\n Code: {code}\n Error: {e}\n"
        return Response({"Log History": serializer.data}, status=status.HTTP_200_OK)
