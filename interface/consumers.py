import json
from channels.generic.websocket import AsyncWebsocketConsumer
from asgiref.sync import async_to_sync
from .models import Player

class LobbyConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.lobby_group_name = 'game_lobby'

        # Juntar-se ao grupo do lobby
        await self.channel_layer.group_add(
            self.lobby_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        # Remover-se do grupo do lobby
        await self.channel_layer.group_discard(
            self.lobby_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        data = json.loads(text_data)

        # Verificar o tipo de mensagem recebida
        if 'type' in data:
            if data['type'] == 'start_game':
                await self.channel_layer.group_send(
                    self.lobby_group_name,
                    {
                        'type': 'start_game',
                    }
                )
            elif 'player_name' in data:
                player_name = data['player_name']
                await self.channel_layer.group_send(
                    self.lobby_group_name,
                    {
                        'type': 'player_joined',
                        'player_name': player_name
                    }
                )
            elif 'player_left' in data:
                player_name = data['player_name']
                await self.channel_layer.group_send(
                    self.lobby_group_name,
                    {
                        'type': 'player_left',
                        'player_name': player_name
                    }
                )
            elif 'character_id' in data:
                character_id = data['character_id']
                await self.channel_layer.group_send(
                    self.lobby_group_name,
                    {
                        'type': 'select_character',
                        'character_id': character_id
                    }
                )
            elif data['type'] == 'wrong_answer':
                await self.channel_layer.group_send(
                    self.lobby_group_name,
                    {
                        'type': 'wrong_answer',
                    }
                )
            elif data['type'] == 'right_answer':
                await self.channel_layer.group_send(
                    self.lobby_group_name,
                    {
                        'type': 'right_answer',
                    }
                )
            elif data['type'] == 'lose_game':
                await self.channel_layer.group_send(
                    self.lobby_group_name,
                    {
                        'type': 'lose_game',
                    }
                )
            elif data['type'] == 'win_game':
                await self.channel_layer.group_send(
                    self.lobby_group_name,
                    {
                        'type': 'win_game',
                    }
                )

    async def player_joined(self, event):
        player_name = event['player_name']

        # Enviar a mensagem para WebSocket
        await self.send(text_data=json.dumps({
            'type': 'player_joined',
            'player_name': player_name
        }))

    async def start_game(self, event):
        await self.send(text_data=json.dumps({
            'type': 'start_game'
        }))

    async def player_left(self, event):
        player_name = event['player_name']

        await self.send(text_data=json.dumps({
            'type': 'player_left',
            'player_name': player_name
        }))

    async def select_character(self, event):
        character_id = event['character_id']

        await self.send(text_data=json.dumps({
            'type': 'select_character',
            'character_id': character_id
        }))

    async def wrong_answer(self, event):
        await self.send(text_data=json.dumps({
            'type': 'wrong_answer'
        }))
    
    async def right_answer(self, event):
        await self.send(text_data=json.dumps({
            'type': 'right_answer'
        }))
    
    async def lose_game(self, event):
        await self.send(text_data=json.dumps({
            'type': 'lose_game',
            'url': '/end_game',
            'message': 'Derrota'
        }))

    async def win_game(self, event):
        await self.send(text_data=json.dumps({
            'type': 'win_game',
            'url': '/end_game',
            'message': 'Vitória'
        }))

    async def room_unlocked(self, event):
        current_room = event['currentRoom']
        next_room = event['nextRoom']
        player_data = event['playerData']

        await self.send(text_data=json.dumps({
            'type': 'room_unlocked',
            'currentRoom': current_room,
            'nextRoom': next_room,
            'playerData': {
                'name': player_data['name'],
                'skin_url': player_data['skin_url']
            }
        }))
