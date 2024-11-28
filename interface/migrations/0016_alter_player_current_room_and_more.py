# Generated by Django 5.1.2 on 2024-11-28 20:28

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('interface', '0015_player_current_room_player_discovered_rooms'),
    ]

    operations = [
        migrations.AlterField(
            model_name='player',
            name='current_room',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='current_player', to='interface.room'),
        ),
        migrations.AlterField(
            model_name='player',
            name='discovered_rooms',
            field=models.ManyToManyField(blank=True, related_name='player', to='interface.room'),
        ),
    ]
