# Generated by Django 5.1.2 on 2024-11-13 21:42

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('interface', '0009_room_skin_hint_room_skin_puzzle'),
    ]

    operations = [
        migrations.AddField(
            model_name='character',
            name='room',
            field=models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='interface.room'),
        ),
    ]
