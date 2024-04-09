from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import async_to_sync
import json
from chipcity.models import Game, Player
from chipcity.views import * 
from chipcity.deck import *
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


            # if ((active_players) > 1):
            #     curr_game = Game.objects.first()
            #     curr_game.players_connected = Player.objects.count()
            #     curr_game.save()
            

        else: 
            pass
        

        self.user = self.scope["user"]
        # self.send(text_data=json.dumps({"message": "i can say whatever i want"}))

        

    def disconnect(self, close_code):
        async_to_sync(self.channel_layer.group_discard)(
            self.group_name, self.channel_name
        )
        curr_game = Game.objects.first()        
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
        

        # want it so that when one player is disconnected, set their active status to false
    
    def initGame(self):
        game_count = Game.objects.all().count()
        if (game_count > 0): 
            print(f"this is the game count: {game_count}")
            games_to_delete = Game.objects.all()
            print(f"these are the games I am deleting: {Game.objects.all()}")
            games_to_delete.delete()
        Game_Action.start_new_game(self,game_id=1,num_users = self.users_connected)
        curr_game = Game.objects.first()
        print(f"ok when i init the game these are the players: {Player.objects.all()}")
        print(f"ok when i init the game these are the games: {Game.objects.all()}")
        print(f"---------------------------------------------------------------------------")
        for player in Player.objects.all():
            print(player)

        curr_game.save()
        flop1_ex = (Game.objects.first().flop1)
        flop2_ex = (Game.objects.first().flop2)
        flop3_ex = (Game.objects.first().flop3)
        turn_ex = (Game.objects.first().turn)
        river_ex = (Game.objects.first().river)
        
        response = flop1_ex + "\n" + flop2_ex + "\n" + flop3_ex + "\n" +turn_ex + "\n" + river_ex
        
        self.send(text_data=json.dumps({"message": response }))
        
        


    def receive(self, **kwargs):
        if 'text_data' not in kwargs:
            self.send_error('you must send text_data')
            return

        try:
            data = json.loads(kwargs['text_data'])
        except json.JSONDecoder:
            self.send_error('invalid JSON sent to server')
            return

        if 'status' not in data:
            self.send_error('status property not sent in JSON')
            return


        status = data['status']
        active_players = 0 
        if(status=="text"):
            for player in Player.objects.all():
                if player.is_active:
                    active_players+=1
            print(f" the number of players is: {active_players}")

            if active_players >= 2:
                print('game initiated')
                self.initGame()
                return
        

        if (status == "waiting"):
                return
        if (status == "inProgress"):
                return
        if (status == "finish"):
                self.finishGame(data)
                return

        self.send_error(f'Invalid status property: "{status}"')

