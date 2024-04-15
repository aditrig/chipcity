from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import async_to_sync
import json
from chipcity.models import Game, Player
from chipcity.views import * 
from chipcity.deck import *
from chipcity.actionhelper import *
import random

class MyConsumer(WebsocketConsumer):
    group_name = 'chipcity_group'
    channel_name = 'game_inProgress'
    users_connected = 0

    user = None
    def send_error(self, error_message):
        self.send(text_data=json.dumps({'error': error_message}))

    def connect(self):
        async_to_sync(self.channel_layer.group_add)(
            self.group_name, self.channel_name
        )

        self.accept()
        player_count = Player.objects.count()
        print(Player.objects.count())

        
        if self.scope['user']:
            self.user = self.scope["user"]
            print("new player created")
            player, created = Player.objects.get_or_create(
                user=self.scope['user'],
                defaults={
                    'game': None,  # Assuming new_game is defined earlier
                    'wallet': 0.00,
                    'seat_number': None,
                    'picture': None,
                    'content_type': None,
                    'is_active': True,  # This is only used if creating a new object
                }
            )
            player.save()


            # If the player was not created, it means it already existed. In this case, only update is_active.
            if not created:
                player.is_active = True
                print(self.user)
                player.save()
                
            for game in Game.objects.all():
                print(game)

        
            active_players = 0 

            print(Player.objects.count())
            for player in Player.objects.all():
                print(player)
                if player.is_active:
                    active_players+=1
                else: print(player)
            print(f"there are this many active players {active_players}")
            print(f"there are this many player objects: {Player.objects.count()}")


            if ((active_players) > 2):
                
                curr_game = Game.objects.first()
                curr_game.save()
            

        else: 
            pass
        

        self.user = self.scope["user"]
        # self.send(text_data=json.dumps({"message": "i can say whatever i want"}))

        

    def disconnect(self, close_code):
        async_to_sync(self.channel_layer.group_discard)(
            self.group_name, self.channel_name
        )      
        print(self.user)
        player = Player.objects.get(user=self.user)
        player.is_active = False
        player.save() 
        print(player.is_active)
        print("websocket is diconnected yay")
        active_players = 0 
        for player in Player.objects.all():
            if player.is_active:
                active_players+=1

        print(f"number of active players: {active_players}")
        curr_game = Game.objects.first()
        curr_game.players_connected = active_players
        curr_game.save()
        

    def play(self): 
        print("playing")
        return
        
        # want it so that when one player is disconnected, set their active status to false
    
    def initGame(self):
        active_players = 0 
        for player in Player.objects.all():
            if player.is_active:
                active_players+=1
        print(f"i am sending game start the number of active players: {active_players}")

        if active_players < 2:
            # Makes sure that game does not start without 2+ players
            return
        
        # Gets list of active players
        list_of_active_players = list_of_players()
        print(list_of_active_players)

        Game_Action.start_new_game(self,1,active_players)
        print(Game.objects.all())

        # Sets BBP and SBP
        curr_game = Game.objects.first()
        # print(curr_game)
        curr_game.small_blind_player = list_of_active_players[0]
        # print(list_of_active_players[1].user)
        curr_game.big_blind_player = list_of_active_players[1]
        curr_game.current_player = list_of_active_players[(list_of_active_players.index(curr_game.big_blind_player)+1)%(curr_game.players_connected)]
        print(f"The Small Blind Player is: {curr_game.small_blind_player}")
        print(f"The Big Blind Player is: {curr_game.big_blind_player}")
        print(f"The Current Player is: {curr_game.current_player}")

        # curr_game = Game.objects.first()
        flop1_ex = (Game.objects.first().flop1)
        flop2_ex = (Game.objects.first().flop2)
        flop3_ex = (Game.objects.first().flop3)
        turn_ex = (Game.objects.first().turn)
        river_ex = (Game.objects.first().river)
        
        
        response = flop1_ex + "\n" + flop2_ex + "\n" + flop3_ex + "\n" +turn_ex + "\n" + river_ex
        
        for hand in Hand.objects.all():
            print(f"This is {hand.player.user}'s hand: {hand.card_left} {hand.card_right}")

        curr_game.save()
        print(response)

        # self.send(text_data=json.dumps({"message": response }))

    def receive(self, **kwargs):
        if 'text_data' not in kwargs:
            self.send_error('you must send text_data')
            return

        try:
            data = json.loads(kwargs['text_data'])
        except json.JSONDecoder:
            self.send_error('invalid JSON sent to server')
            return

        if 'action' not in data:
            self.send_error('status property not sent in JSON')
            return


        status = data['action']
        active_players = 0 
        if(status=="ready"):
            for player in Player.objects.all():
                if player.is_active:
                    active_players+=1
            print(f" the number of players is: {active_players}")

            if (active_players >= 2 and Game.objects.count() == 0):
                print('game initiated')
                self.initGame()
                return
            community_cards = Game.objects.first().flop1 + "\n" + Game.objects.first().flop2 + "\n" + Game.objects.first().flop3 + "\n" +Game.objects.first().turn + "\n" + Game.objects.first().river
            print(community_cards)
            
            for hand in Hand.objects.all():
                print(f"This is {hand.player.user}'s hand: {hand.card_left} {hand.card_right}")
            
            return
        

        if (status == "start"):
                if (Game.objects.count() ==1):
                    self.play() 
                    return
        if (status == "inProgress"):
                return
        if (status == "finish"):
                self.finishGame(data)
                return

        else: self.send_error(f'Invalid status property: "{status}"')

