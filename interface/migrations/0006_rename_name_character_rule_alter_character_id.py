# Generated by Django 5.1.2 on 2024-11-11 21:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('interface', '0005_alter_player_id'),
    ]

    operations = [
        migrations.RenameField(
            model_name='character',
            old_name='name',
            new_name='rule',
        ),
        migrations.AlterField(
            model_name='character',
            name='id',
            field=models.AutoField(primary_key=True, serialize=False),
        ),
    ]
