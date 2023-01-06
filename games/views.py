from django.shortcuts import get_object_or_404, render
from .models import Game
import requests as req
import xml.etree.ElementTree as ET

def fill_bgg_data(game, player_count):
    if game.bgg_id == 0:
        game.thumbnail = 'https://upload.wikimedia.org/wikipedia/commons/8/8d/CH-Gefahrensignal-Baustelle.svg'
        return game

    # Query BGG API
    url = 'https://boardgamegeek.com/xmlapi2/thing?id={}&stats=1'.format(game.bgg_id)
    response = req.get(url)

    if response.status_code != 200:
        print('BGG response: {}, {}'.format(response.status_code, response.reason))
        game.thumbnail = 'https://upload.wikimedia.org/wikipedia/commons/0/01/Vienna_Convention_road_sign_Aa-32-V1.svg'
        return game

    bgg_xml_data = ET.fromstring(response.text)

    # Thumbnail
    thumbnail_element = bgg_xml_data.find('item/thumbnail')
    if thumbnail_element is not None:
        game.thumbnail = thumbnail_element.text

    # Rating
    average_rating_element = bgg_xml_data.find('item/statistics/ratings/average')
    if average_rating_element is not None:
        rating = float(average_rating_element.get('value'))
        game.rating = round(rating, 1)

    # Weight
    average_weight_element = bgg_xml_data.find('item/statistics/ratings/averageweight')
    if average_weight_element is not None:
        weight = float(average_weight_element.get('value'))
        game.weight = round(weight, 1)

    # Best player count and recommended for the requested count
    # TODO: this would look better with an XPath (item/poll[name='suggested bla bla'])
    polls = bgg_xml_data.findall('item/poll')
    players_count_poll = None
    for poll in polls:
        if poll is not None and poll.get('name') == 'suggested_numplayers':
            players_count_poll = poll
            break
    if players_count_poll is not None:
        # Find best players count
        best_numplayers_votes = -1
        for results in players_count_poll.findall('results'):
            if results is not None:
                for result in results.findall('result'):
                    if result.get('value') == 'Best':
                        votes = int(result.get('numvotes'))
                        if votes > best_numplayers_votes:
                            best_numplayers_votes = votes
                            game.opt_players = int(results.get('numplayers'))
        # Find if this player count is recommended
        for results in players_count_poll.findall('results'):
            if results is not None and results.get('numplayers') == str(player_count):
                votes_recommend = 0
                votes_not_recommend = 0
                for result in results.findall('result'):
                    if result.get('value') == 'Recommended':
                        votes_recommend = int(result.get('numvotes'))
                    elif result.get('value') == 'Not Recommended':
                        votes_not_recommend = int(result.get('numvotes'))
                game.recommended_players = votes_recommend > votes_not_recommend

    return game

def index(request):

    games_list = Game.objects.order_by('?').all()
    player_count = 0
    if request.method == 'POST':
        try:
            player_count = int(request.POST['player_count'])
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

    # Convert our games list into one with data from BGG
    games_list = list(map(lambda game: fill_bgg_data(game, player_count), games_list))

    # Sort by matching opt player count, then recommended, then by rating
    if player_count != 0:
        games_list = sorted(
            games_list,
            reverse=True,
            key=lambda e: (
                1 if e.opt_players == player_count else 0,
                1 if e.recommended_players else 0,
                e.rating
            ))

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