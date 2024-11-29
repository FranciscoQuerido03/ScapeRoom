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
    'Sotao' : 'Xxyowi5wEloR',
    'CasaDeBanho' : 'ONLh8LwgN8oN',
    'Escritorio' : 'BAlzmc9z282p',
    'Bercario' : 'MZlqqrfMoKZv',
    'Hall': 'A7F9K2L8T3Z6',
}

Acoes = [
    "You can only communicate by saying YES and NO.",
    "You can only communicate by gestures",
    "You can only communicate by lying",
    "You can only communicate when someone calls you",
]

Acoes_used = []

Counter = 0

@csrf_exempt
def render_room(request):
    try:
        data = json.loads(request.body)
        player_id = data.get('player')
        direcao = data.get('direcao')

        if not player_id or not direcao:
            return JsonResponse({'error': 'Dados inválidos'}, status=400)

        # Obter o jogador e a sala atual
        player = Player.objects.filter(id=player_id).first()
        current_room = player.character.room

        # Obter as salas descobertas e ordená-las
        discovered_rooms = list(player.discovered_rooms.all())

        # Determinar a posição da sala atual
        try:
            current_index = discovered_rooms.index(current_room)
        except ValueError:
            return JsonResponse({'error': 'Sala atual não encontrada nas descobertas'}, status=404)

        # Determinar a próxima sala com base na direção
        if direcao == 'esquerda' and current_index > 0:
            next_room = discovered_rooms[current_index - 1]
        elif direcao == 'direita' and current_index < len(discovered_rooms) - 1:
            next_room = discovered_rooms[current_index + 1]
        else:
            return JsonResponse({'error': 'Movimento inválido'}, status=400)
        
        

        # Atualizar a sala do jogador
        player.character.room = next_room
        player.character.save()

        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            'game_lobby', 
            {
                'type': 'change_room',
                'currentRoom': current_room.name,
                'nextRoom': next_room.name,
                'playerData': {
                    'name': player.name,
                    'skin_url': player.character.avatar.url,
                }
            }
        )

        next_room_url = '/game/' + next_room.name + '/'+ Access_Code[next_room.name]

        return JsonResponse({'redirect_url': next_room_url})

    except json.JSONDecodeError:
        return JsonResponse({'error': 'JSON inválido'}, status=400)
    
@csrf_exempt
def render_join(request):
    return render(request, 'join_game.html')

@csrf_exempt
def render_wait_room(request):
    return render(request, 'wait_room.html')

@csrf_exempt
def render_shared(request):
    players = Player.objects.all()
    rooms = {
        "Bercario": None,
        "Escritorio": None,
        "CasaDeBanho": None,
        "Cozinha": None,
        "Sala": None,
        "Sotao": None,
        "Quarto": None,
        "Garagem": None,
    }

    for player in players:
        room_name = player.character.room.name
        if room_name in rooms:  # Apenas se o nome da sala estiver na lista
            rooms[room_name] = {
                'name': player.name,
                'skin_url': player.character.avatar.url
            }

    return render(request, 'shared_screen.html', {'rooms': rooms})

@csrf_exempt
def render_select_char(request):
    players = Player.objects.all()
    characters_used = []
    
    for player in players:
        if player.character:
            characters_used.append(player.character.id)

    return render(request, 'select_char.html', {
        'characters_used': characters_used,
        'character_ids': range(1, 9)  # Gera os IDs de 1 a 8
    })


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
def render_game_room(request, room_name, key):

    if room_name not in Access_Code or key != Access_Code[room_name]:
        if key in Access_Code.values():
            room_name = next(room for room, code in Access_Code.items() if code == key)
        else:
            print("Tentativa de malandragem")
            return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))


    room = Room.objects.filter(name=room_name).first()  # Get the first Room object with the given name
    character = Character.objects.filter(room=room).exclude(rule="default").first()
    player = Player.objects.filter(character=character).first()

    if not room:
        print("Erro na sala")
        return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
    
    if room.perms:
        print("Last Room")
        print(room.name)
        print(character.rule)
        character.last_room = True
        character.save()

    context = {
        'room_name': room_name,
        'room_skin': room.skin.url,
        'room_hint_skin': room.skin_hint.url,
        'room_puzzle_skin': room.skin_puzzle.url,
        'rule': character.rule,
        'color': character.color,
        'skin': character.skin.url,
    }
    
    # Obter as salas descobertas
    discovered_rooms = list(player.discovered_rooms.all())

    if len(discovered_rooms) > 1: 
        current_index = discovered_rooms.index(room)
        
        if current_index == 0:  # Primeira sala
            context['right_arrow'] = True
        elif current_index == len(discovered_rooms) - 1:  # Última sala
            context['left_arrow'] = True
        else:  # Sala do meio
            context['right_arrow'] = True
            context['left_arrow'] = True
    
    return render(request, 'game_room.html', context)

@csrf_exempt
def render_end(request, message):
    context = {'message': message}
    return render(request, 'end_game.html', context)

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
        data = json.loads(request.body)
        player_id = data.get('playerId')
        character_id = data.get('characterId')

        player = Player.objects.get(id=player_id)
        character = Character.objects.get(id=character_id)

        room = Room.objects.filter(perms=False, ocupied=False, final=False).first() #Perms = false significa sala incial para mudança de sala procurar pelas perms = true

        character.room = room

        player.character = character

        player.discovered_rooms.add(room)
        player.current_room = room

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

        player.save()
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
    Character.objects.update(last_room=False)
    global Counter
    global Acoes_used
    Counter = 0
    Acoes_used = []
    return render(request, 'join_game.html')

@csrf_exempt
def check_answer(request):
    data = json.loads(request.body)
    room_name = data.get('room_name')
    answer = data.get('answer')
    player_id = data.get('player_id')

    room = Room.objects.filter(name=room_name).first()
    player = Player.objects.filter(id=player_id).first()
    character = player.character

    if not room:
        return HttpResponseForbidden()

    if answer == room.answer:
        print('Resposta correta')

        if character.last_room:
            print("3 sala")
            global Counter
            Counter += 1
            next_room = Room.objects.filter(final=True).first()

        else:
            print("2 sala")
            # Marcar a sala atual como desocupada
            room.ocupied = False
            room.save()

            # Encontrar a próxima sala disponível
            next_room = Room.objects.filter(perms=True, ocupied=False, final=False).exclude(name=room.answers_to.name).first()

        # Atualizar a próxima sala para ocupada
        if next_room:
            next_room.ocupied = True
            next_room.save()

            player.character.room = next_room
            character.room = next_room

            player.discovered_rooms.add(next_room)
            player.current_room = next_room

            player.save()
            character.save()

            # Configurar a camada de canal
            channel_layer = get_channel_layer()
            
            # Enviar mensagem para o grupo do WebSocket
            async_to_sync(channel_layer.group_send)(
                'game_lobby', 
                {
                    'type': 'room_unlocked',
                    'currentRoom': room_name,
                    'nextRoom': next_room.name,
                    'playerData': {
                        'name': player.name,
                        'skin_url': player.character.avatar.url,
                    }
                }
            )

            async_to_sync(channel_layer.group_send)(
                'game_lobby', 
                {
                    'type': 'right_answer',
                }
            )

            # Preparar o código de acesso para a próxima sala
            key = Access_Code[next_room.name]

            # Preparar o contexto para enviar de volta como resposta HTTP
            context = {
                'room_name': next_room.name,
                'key': key,
            }
            
            return JsonResponse({'success': True, 'context': context})
    
    # Caso a resposta esteja incorreta, enviar uma notificação de resposta errada
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        'game_lobby', 
        {
            'type': 'wrong_answer',
            'message': 'Resposta incorreta'
        }
    )

    return JsonResponse({'success': False})