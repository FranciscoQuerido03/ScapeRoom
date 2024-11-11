from django.views.decorators.csrf import csrf_exempt
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from django.http import JsonResponse
from django.shortcuts import render
from .models import Player
import json

# acoes_personagem = [
#     "Só falar na negativa",
#     "Só falar na positiva",
#     "Só falar em perguntas",
#     "Só falar em exclamações",
#     "Só falar em ordens",
# ]

# acoes_used = []

# Create your views here.
@csrf_exempt
def render_room(request):
    player =  Player.objects.filter(request.GET.get('player'))
    room = player.character.room.name
    room_name = room + '.html'
    return render(request, room_name)

@csrf_exempt
def render_join(request):
    return render(request, 'join_game.html')

@csrf_exempt
def render_wait_room(request):
    return render(request, 'wait_room.html')

@csrf_exempt
def render_shared(request):
    return render(request, 'shared_screen.html')

@csrf_exempt
def render_select_char(request):
    return render(request, 'select_char.html')

@csrf_exempt
def render_lobby_view(request):
    players = Player.objects.all() 
    return render(request, 'lobby.html', {'players': players})

@csrf_exempt
def register(request):
    player_name = request.POST.get('player_name')
    player = Player.objects.create(name=player_name)
    player.save()

    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        'game_lobby', 
        {
            'type': 'player_joined',
            'player_name': f'{player_name}'
        }
    )
    # Cria a resposta JSON com o ID do jogador
    response_data = {'player': player.id}
    print(response_data)
    
    return JsonResponse(response_data)

@csrf_exempt
def finish_game(request):
    Player.objects.all().delete()
    return render(request, 'join_game.html')

@csrf_exempt
def leave_game(request):
    data = json.loads(request.body)
    player_id = data.get('player_id')
    player = Player.objects.get(id=player_id)
    player_name = player.name
    player.delete()

    
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        'game_lobby', 
        {
            'type': 'player_left',
            'player_name': f'{player_name}'
        }
    )

    return render(request, 'join_game.html')
