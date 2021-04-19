from .models import *


def delete_already_created_games(view_func):
    def wrapper_func(request, *args, **kwargs):
        if 'created_game' in request.session.keys() and request.session['created_game'] is not None:
            game = Game.objects.get(name=request.session['created_game'])
            game.delete()
        return view_func(request, *args, **kwargs)
    return wrapper_func


def change_current_users_of_games(view_func):
    def wrapper_func(request, *args, **kwargs):
        if 'joined_game' in request.session.keys() and request.session['joined_game'] is not None:
            game = Game.objects.get(name=request.session['joined_game'])
            game.current_players = 1
            game.save()
        return view_func(request, *args, **kwargs)
    return wrapper_func
