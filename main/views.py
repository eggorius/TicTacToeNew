from django.shortcuts import render, redirect, reverse
from .models import *
from django.core import serializers
from .forms import CreateGameForm
from .decorators import *
import json


def parse_tegify_tags(tags_titles):
    tags_titles = json.loads(tags_titles)
    tags_titles_parsed = [t["value"] for t in tags_titles]
    return tags_titles_parsed


#@delete_already_created_games
@change_current_users_of_games
def index(request):
    request.session['created_game'] = None  # means this user hasnt created a game
    request.session['joined_game'] = None

    json_serializer = serializers.get_serializer("json")()
    all_tags = json_serializer.serialize(Tag.objects.all(), ensure_ascii=False)
    if request.method == 'POST':
        if 'find' in request.POST:
            tags_titles = request.POST.get('tags-jquery')
            if len(tags_titles) != 0:
                tags_titles_parsed = parse_tegify_tags(tags_titles)
                tags = Tag.objects.filter(title__in=tags_titles_parsed)
                games = set(Game.objects.filter(tags__in=tags))
                context = {
                    'games': games,
                    'tags': all_tags,
                }
                return render(request, 'main/index.html', context)
            games = Game.objects.all()
            return render(request, 'main/index.html', {'games': games, 'tags': all_tags})
        if 'create' in request.POST:
            form = CreateGameForm(request.POST)
            if form.is_valid():
                game = form.save()
                tags_title = request.POST.get('tags-input')
                tags_title_parsed = parse_tegify_tags(tags_title)
                for tag in tags_title_parsed:
                    t = Tag(title=tag)
                    t.save()
                    game.tags.add(t)
                print(game.name)
                game.save()
                request.session['created_game'] = game.name  # means this user has created a game
                return redirect(reverse('join_game', kwargs={'name': game.name}))
            return redirect('home')

    form = CreateGameForm()
    games = Game.objects.all()
    return render(request, 'main/index.html', {'games': games, 'tags': all_tags, 'form': form})


def join_game(request, name):
    game = Game.objects.get(name=name)
    if game.current_players == 2:
        return redirect('home')
    if request.session['created_game'] is not None:
        print('FROM 1: ', 'created_game' in request.session.keys())
        player = 'x'
    else:
        print('FROM 2: ', 'created_game' in request.session.keys())
        request.session['joined_game'] = name
        game.current_players = 2
        game.save()
        player = 'o'
    return render(request, 'main/game.html', {'game_name': name, 'player': player})


def leave_game(request):
    pass
