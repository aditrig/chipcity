from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import async_to_sync
import json
from chipcity.models import Game, Player
from chipcity.views import * 
from chipcity.deck import *
import random



class MyConsumer(WebsocketConsumer):
    group_name = 'chipcity_group'
    channel_name = 'chipcity_channel'

    user = None
    
    def send_error(self, error_message):
        self.send(text_data=json.dumps({'error': error_message}))

    def connect(self):
        async_to_sync(self.channel_layer.group_add)(
            self.group_name, self.channel_name
        )

        self.accept()
        
        if self.scope['user']:
            print(self.scope['user'])
            self.user = self.scope["user"]
            new_game = Game.objects.first()
            new_game.players_connected +=1
            print("new_game.players_connected" + str(new_game.players_connected) )
            new_game.save()
            # new_player = Player.objects.get_or_create(user=self.scope['user'])
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

            # If the player was not created, it means it already existed. In this case, only update is_active.
            if not created:
                player.is_active = True
                player.save()

            # try:
            #     # Try to get the existing player
            #     existing_player = Player.objects.get(user=self.scope['user'])
            #     # If the player exists, set is_active to True
            #     existing_player.is_active = True
            #     existing_player.save()
            # except Player.DoesNotExist:
            #     # If the player does not exist, create a new one
            #     new_game = Game.objects.first()
            #     new_player = Player(
            #         user=self.scope['user'], 
            #         game=new_game, 
            #         wallet=0.00, 
            #         seat_number=new_game.players_connected, 
            #         picture=None, 
            #         content_type=None, 
            #         is_active=True
            #     )
            #     new_player.save()
            # if (Player.objects.get(user=self.scope['user']) == None):
            #     new_player = Player(user=self.scope['user'], game = new_game, wallet = 0.00, seat_number = new_game.players_connected, picture = None, content_type = None, is_active = True)
            #     new_player.save()
            # else:
            #     Player.objects.get(user=self.scope['user']).is_active = True
            # print(Player.objects.first())
            # print(Player.objects.count())
            # print(new_game.players_connected)
        else: 
            pass
        
        #     add user to Connected model
        #     await connect_user(room_name=self.room_name, user=self.scope['user'], channel_name=self.channel_name)


        # if not self.scope["user"].is_authenticated:
        #     self.send_error(f'You must be logged in')
        #     print("closing")
        #     # self.close()
        #     return      

        self.user = self.scope["user"]
        # self.send(text_data=json.dumps({"message": "i can say whatever i want"}))

        

    def disconnect(self, close_code):
        async_to_sync(self.channel_layer.group_discard)(
            self.group_name, self.channel_name
        )
        print('when disconnected, delete a player')
        curr_game = Game.objects.first()
        curr_game.players_connected -= 1
        print('players connected after disconnected user' + str(curr_game.players_connected))
        print("The number of games:" + str(curr_game.players_connected))
        
        player = Player.objects.get(user=self.user)
        player.is_active = False
        # want it so that when one player is disconnected, set their active status to false
    
    def initGame(self):
        game_count = Game.objects.all().count()
        if (game_count > 0): 
            print(game_count)
            games_to_delete = Game.objects.all()
            print(Game.objects.all())
            games_to_delete.delete()
        print("hi?")
        Game_Action.start_new_game(self,game_id=1)
        curr_game = Game.objects.first()
        print('initialized game and see how many players')
        print("the number of players currently connected is:" + str(curr_game.players_connected))
        print(Player.objects.all())
        print(Game.objects.all())
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

        if 'action' not in data:
            self.send_error('action property not sent in JSON')
            return


        action = data['action']
        
        if(action=="text"):
            print(Game.objects.first().players_connected)
            if (len(Player.objects.all()) > 0):
                print('game initiated')
                self.initGame()
            return
        
        if (action == "reset"):
            curr_game = self.initGame()

        if (action == "waiting"):
                    return
        if (action == "finish"):
                self.finishGame(data)
                return

        self.send_error(f'Invalid action property: "{action}"')

