# Generated by Django 5.1.2 on 2024-11-04 16:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('interface', '0003_alter_player_character'),
    ]

    operations = [
        migrations.CreateModel(
            name='Session',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('players', models.ManyToManyField(to='interface.player')),
            ],
        ),
    ]