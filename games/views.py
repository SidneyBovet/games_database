from django.shortcuts import get_object_or_404, render
from .models import Game

def index(request):

    games_list = Game.objects.order_by('?').all()
    player_count = 0
    if request.method == 'POST':
        try:
            player_count = pk=request.POST['player_count']
            games_list = Game.objects.order_by('?').filter(
                min_players__lte=player_count,
                max_players__gte=player_count
            )
        except KeyError:
            return render(request, 'games/index.html', {
                'games_list': games_list,
                'error_message': "You didn't provide a number of players.",
            })
        except ValueError:
            return render(request, 'games/index.html', {
                'games_list': games_list,
                'error_message': "Try giving an actual number of players.",
            })

    context = {
        'games_list': games_list,
        'player_count': player_count,
    }
    return render(request, 'games/index.html', context)


def detail(request, game_id):
    game = get_object_or_404(Game, pk=game_id)
    context = {
        'game': game,
    }
    return render(request, 'games/detail.html', context)