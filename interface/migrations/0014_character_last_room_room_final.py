# Generated by Django 5.1.2 on 2024-11-17 01:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('interface', '0013_character_color'),
    ]

    operations = [
        migrations.AddField(
            model_name='character',
            name='last_room',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='room',
            name='final',
            field=models.BooleanField(default=False),
        ),
    ]
