from django.shortcuts import render
from .models import Player

# Create your views here.

def render_lobby(request):
    return render(request, 'lobby.html')

def render_room(request):
    player =  Player.objects.filter(request.GET.get('player'))
    room = player.character.room.name
    room_name = room + '.html'
    return render(request, room_name)

