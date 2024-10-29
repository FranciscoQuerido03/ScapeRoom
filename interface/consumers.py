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
                # Enviar mensagem para todos no grupo do lobby
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
