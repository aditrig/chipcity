# Generated by Django 5.0.1 on 2024-04-01 22:55

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('chipcity', '0007_game_curr_round_game_flop1_game_flop2_game_flop3_and_more'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Card',
            new_name='StuffCard',
        ),
    ]
