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
        # we need to instantiate a Player object
        # number of connected users in game object field, if ==1 then call the game_init function

        self.accept()
        
        print("def connect line 24")
        if self.scope['user']:
            print("about to make game 26")

            new_game = Game.objects.first()
            new_game.players_connected+=1 
            new_game.save()
            print(new_game.players_connected)
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
        print("ok so")
        self.send(text_data=json.dumps({"message": "i can say whatever i want"}))

        

    def disconnect(self, close_code):
        async_to_sync(self.channel_layer.group_discard)(
            self.group_name, self.channel_name
        )
    
    def initGame(self):
        print("huhiubo")

        game = Game.objects.first()
        new_deck = Deck.GetFullDeck()
        indices = random.sample(range(0, 52), 5)
        game.flop1 = new_deck[indices[0]]
        game.flop2 = new_deck[indices[1]]
        game.flop3 = new_deck[indices[2]]
        game.turn = new_deck[indices[3]]
        game.river = new_deck[indices[4]]
        for i in indices:
            new_deck.pop(new_deck[i])
        return

    def receive(self, **kwargs):
        print("hii")
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
        words = data['text']
        
        if(action=="text"):
            self.send(text_data=json.dumps({"message": words}))
            print("why no if")
            print(Game.objects.first().players_connected)
            if (Game.objects.first().players_connected > 1):
                
                self.initGame()
                print("is init game")
                return

            return

            
        
        if (action == "waiting"):

                print("we here")
                if (Game.objects.first().players_connected == 1):
                    self.initGame()
                    return
        if (action == "finish"):
                self.finishGame(data)
                return

        self.send_error(f'Invalid action property: "{action}"')

