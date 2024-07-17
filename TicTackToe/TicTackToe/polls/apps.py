from django.apps import AppConfig

class TicTackToeConfig(AppConfig):
    '''
        this class is used when the app starts up 
    '''
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'TicTackToe'
    
