from django.shortcuts import render
from django.core.exceptions import ObjectDoesNotExist
from django.views.decorators.http import require_GET
from requests import post
from django.http import JsonResponse
from .models import Vote, Game, PriceShown, AverageValue

def get_games(search="", page=0):
    games = list(Game.objects.filter(name__startswith=search).order_by('id')[page*12:(page+1)*12])
    if len(games) < 12:
        # response = post('https://api.igdb.com/v4/games', **{'headers': {'Client-ID': 'wgui54tmmai7nhqkte8xtq2bphlexn', 'Authorization': 'Bearer nabq72dt0byopszz4v6gf970t3sxbp'},'data': 'fields id, name; where rating_count > 100;'})
        response = post('https://api.igdb.com/v4/games', **{'headers': {'Client-ID': 'wgui54tmmai7nhqkte8xtq2bphlexn', 'Authorization': 'Bearer nabq72dt0byopszz4v6gf970t3sxbp'},'data': 'search "' + search + '"; fields id, name, artworks; where rating_count > 100; limit 100;'})
        json = response.json()

        for x in json:
            try: 
                res = Game.objects.get(id=x['id'])
            except ObjectDoesNotExist:
                games.append(Game.objects.create(id= x['id'], name=x['name']))



    return games

# Create your views here.
def browse(request):
    search = request.GET.get('search', '')
    page = int(request.GET.get('page', 0))
    games = get_games(search, page)
    if(len(games) == 0):
        return render(request, "error.html", {"error": "Your search for " + search + " returned nothing. Perhaps did you mispell what you were looking for?"})
    context = {'games': games}
    return render(request, "index.html", context)

def game(request, game_id):
    try:
        game = Game.objects.get(id=game_id)
    except:
        game = {'name': game_id + ' Does not exist.', 'price': '$9.99'}

    try:
        value = "$" + str(AverageValue.objects.get(game_id=game).value)
    except:
        value = "$-99.99"

    if request.user.is_authenticated:
        try:
            ps = PriceShown.objects.get(game=game, user_id=request.user)
        except:
            ps = PriceShown.objects.create(game=game, user=request.user, value=10)

    context = {'game': game, "value": value }
    return render(request, "game.html", context)

def update_vote(request, game_id, user_id, multiplier):
    try:
        multiplier = float(multiplier)
        if multiplier < -2 or multiplier > 2:
            return JsonResponse({"error": "Multiplier must be in the range -2 to 2"}, status=400)
    except ValueError:
        return JsonResponse({"error": "Multiplier must be a valid floating-point number"}, status=400)

    try:
        vote = Vote.objects.get(game_id=game_id, user_id=user_id)
        vote.value += multiplier * vote.value
        vote.save()
        return JsonResponse({"success": True})
    except Vote.DoesNotExist:
        # Create a new vote if it doesn't exist
        Vote.objects.create(game_id=game_id, user_id=user_id, value=multiplier)
        return JsonResponse({"success": True, "message": "New vote created"})