from django.db import connection, DatabaseError
from django.core.management import call_command
from django.db import migrations
from .models import Game  # Import your Game model
from rest_framework import viewsets, status
from rest_framework.decorators import api_view
from rest_framework.response import Response

class GameViewSet(viewsets.ModelViewSet):
    def create_game_table(self):
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
                
                # Create initial game entities if needed
                if not Game.objects.exists():
                    Game.objects.create(history=[[""]*9], current_move=0)
                print("Game table created successfully.")
            else:
                print("Game table already exists.")
        
        except DatabaseError as e:
            # Handle database errors
            print(f"Error creating game table: {e}")

    def get_queryset(self):
        return Game.objects.all()

    def get_serializer_class(self):
        return GameSerializer

gvs = GameViewSet()  # Instantiate GameViewSet

@api_view(['GET'])
def start_game(request):
    try:
        # Ensure the game table is created if not already
        gvs.create_game_table()
        # Create a new game instance
        game = Game.objects.create(history=[[""]*9], current_move=0)
        return Response({"message": "Game started", "game_id": game.id}, status=status.HTTP_201_CREATED)
    except Exception as e:
        # Handle any exceptions that occur during game creation
        print(f"Error starting game: {e}")
        return Response({"error": "Failed to start game"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET', 'POST'])
def clean_database(request):
    """
    Cleans the database by removing any anomaly data or unused data.

    Parameters:
    - request: The HTTP request used to trigger the database cleaning process.
    """
    pass

@api_view(['GET', 'POST'])
def logging(request):
    """
    Logs the game events.

    Parameters:
    - request: The HTTP request containing data to be logged.
    """
    pass

