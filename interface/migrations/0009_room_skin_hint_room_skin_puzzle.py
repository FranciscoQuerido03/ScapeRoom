# Generated by Django 5.1.2 on 2024-11-13 02:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('interface', '0008_room_skin_alter_room_perms'),
    ]

    operations = [
        migrations.AddField(
            model_name='room',
            name='skin_hint',
            field=models.ImageField(default='skins/default_image.jpg', upload_to='skins/'),
        ),
        migrations.AddField(
            model_name='room',
            name='skin_puzzle',
            field=models.ImageField(default='skins/default_image.jpg', upload_to='skins/'),
        ),
    ]
