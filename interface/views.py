from django.views.decorators.csrf import csrf_exempt
from channels.layers import get_channel_layer
from django.shortcuts import render, redirect
from django.http import HttpResponseForbidden, HttpResponseRedirect
from asgiref.sync import async_to_sync
from .models import Player, Character, Room
from django.http import JsonResponse
from urllib.parse import quote
import json

Access_Code = {
    'Cozinha' : 'cYxICODn1fkb',
    'Sala' : 'zlqE44O6cr9Z',
    'Quarto' : 'y2bwIsMuoxqX',
    'Garagem' : '0ynZXbTMmh0x',
    'Zona da brincadeira' : 'Xxyowi5wEloR',
    'Casa de banho' : 'ONLh8LwgN8oN',
    'Escritorio' : 'BAlzmc9z282p',
    'Berçario' : 'MZlqqrfMoKZv',
}

Acoes = [
    "So pode falar sim e nao",
    "So gestos",
    "So NSFW",
    "Especialista em BitCoin"
]

Acoes_used = []


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
def render_char_specs(request, char_rule, char_url):  
    context = {
        'character_acao': char_rule,
        'character_image': char_url,
    }
    return render(request, 'character_specs.html', context)


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
def associate_char(request):
    if request.method == 'POST':
        # Decodificar o corpo JSON da requisição
        data = json.loads(request.body.decode('utf-8'))
        player_id = data.get('playerId')
        character_id = data.get('characterId')

        print(player_id)

        player = Player.objects.get(id=player_id)
        character = Character.objects.get(id=character_id)

        player.character = character

        room = Room.objects.filter(perms=False, ocupied=False).first() #Perms = false significa sala incial para mudança de sala procurar pelas perms = true
        print(room.name)

        if room:
            room.ocupied = True
            room.save()

            room_name = room.name
            room_url = room.skin.url

        for i in Acoes: 
            if i not in Acoes_used:
                Acoes_used.append(i)
                acao = i
                break


        image_url = character.skin.url
        character.rule = acao
        character.save()

        # Envia uma mensagem ao WebSocket (presumindo que a parte do WebSocket esteja funcionando)
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            'game_lobby', 
            {
                'type': 'select_character',
                'character_id': character.id
            }
        )

        key = Access_Code[room_name]

        # Preparando o contexto para enviar para o template
        context = {
            'character_acao': acao,
            'character_image': image_url,
            'room_name': room_name,
            'key': key,
        }

        return JsonResponse(context)

@csrf_exempt
def finish_game(request):
    Player.objects.all().delete()
    Character.objects.update(rule='default')
    Room.objects.update(ocupied=False)
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


@csrf_exempt
def render_game_room(request, room_name, key):

    if room_name not in Access_Code or key != Access_Code[room_name]:
        if key in Access_Code.values():
            room_name = next(room for room, code in Access_Code.items() if code == key)
        else:
            print("Tentativa de malandragem")
            return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))

    room = Room.objects.filter(name=room_name).first()

    if not room:
        print("Erro na sala")
        return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))

    context = {
        'room_name': room_name,
        'room_skin': room.skin.url,
        'room_hint_skin': room.skin_hint.url,
        'room_puzzle_skin': room.skin_puzzle.url,
    }
    
    return render(request, 'game_room.html', context)