from django.contrib import admin

# Register your models here.

from .models import Player, Character

admin.site.register(Player)
admin.site.register(Character)