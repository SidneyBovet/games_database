from django.http import Http404, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from .models import Game, Genre, Type

def index(request):
    
    games_list = Game.objects.all()
    if request.method == 'POST':
        try:
            player_count = pk=request.POST['player_count']
            games_list = Game.objects.filter(
                min_players__lte=player_count,
                max_players__gte=player_count
            )
        except (KeyError):
            return render(request, 'polls/index.html', {
                'games_list': games_list,
                'error_message': "You didn't give a number of players.",
            })

    context = {
        'games_list': games_list,
    }
    return render(request, 'games/index.html', context)

def detail(request, game_id):
    game = get_object_or_404(Game, pk=game_id)
    context = {
        'game': game,
    }
    return render(request, 'games/detail.html', context)