# Generated by Django 5.1.2 on 2024-11-11 21:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('interface', '0006_rename_name_character_rule_alter_character_id'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='character',
            name='room',
        ),
        migrations.AlterField(
            model_name='character',
            name='rule',
            field=models.CharField(max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='character',
            name='skin',
            field=models.ImageField(upload_to='skins/'),
        ),
    ]