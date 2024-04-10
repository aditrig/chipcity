from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import async_to_sync
import json
from chipcity.models import Game, Player
from chipcity.views import * 
from chipcity.deck import *
import random

def play():
    # # Assuming that community cards and each hand for each active player have been dealt, 
    # # we want to check the round, and set the big blind, small blind, and first player
    # curr_game = Game.objects.first()
    # curr_round = curr_game.curr_round 
    
    # if (curr_round == 0): 
    #     round_action()
    # if (curr_round == 1): 
    #     round_action()
    # if (curr_round == 2): 
    #     round_action()
    # if (curr_round == 3): 
    #     round_action()
        
    # curr_game.curr_round += 1
    # curr_round.save()
    return