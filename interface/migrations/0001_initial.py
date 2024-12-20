# Generated by Django 5.1.2 on 2024-10-28 17:30

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Room',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('ocupied', models.BooleanField(default=False)),
                ('perms', models.IntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='Puzzle',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('skin', models.ImageField(default='skins/default.png', upload_to='skins/')),
                ('solution', models.CharField(max_length=50)),
                ('room', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='interface.room')),
            ],
        ),
        migrations.CreateModel(
            name='Item',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('skin', models.ImageField(default='skins/default.png', upload_to='skins/')),
                ('room', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='interface.room')),
            ],
        ),
        migrations.CreateModel(
            name='Character',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('skin', models.ImageField(default='skins/default.png', upload_to='skins/')),
                ('room', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='interface.room')),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('character', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='interface.character')),
            ],
        ),
    ]
