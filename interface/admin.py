from django.contrib import admin

# Register your models here.

from .models import Player, Character, Room

admin.site.register(Player)
admin.site.register(Character)
admin.site.register(Room)