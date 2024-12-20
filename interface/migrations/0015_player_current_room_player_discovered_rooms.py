# Generated by Django 5.1.2 on 2024-11-28 19:52

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('interface', '0014_character_last_room_room_final'),
    ]

    operations = [
        migrations.AddField(
            model_name='player',
            name='current_room',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='current_players', to='interface.room'),
        ),
        migrations.AddField(
            model_name='player',
            name='discovered_rooms',
            field=models.ManyToManyField(blank=True, related_name='players', to='interface.room'),
        ),
    ]
