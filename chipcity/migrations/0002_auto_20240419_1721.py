# Generated by Django 3.2.24 on 2024-04-19 17:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chipcity', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='game',
            name='list_of_active_players',
        ),
        migrations.AddField(
            model_name='player',
            name='spectator',
            field=models.BooleanField(default=False),
        ),
    ]
