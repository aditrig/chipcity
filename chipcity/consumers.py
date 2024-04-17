from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import async_to_sync
import json
from chipcity.models import Game, Player, Hand
from chipcity.views import * 
from chipcity.deck import *
from chipcity.actionhelper import *
import random

from django.http import JsonResponse
from django.forms.models import model_to_dict


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
                    'wallet': 0.00,
                    'seat_number': None,
                    # 'picture': None,
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
        
    
    def isGameOver(self):
        game = Game.objects.first()
        if game.curr_round == 4:
            # showdown
            return True
        num_active_players = Player.objects.all().filter(is_active = True).count()
        is_all_in_count = 0
        for player in Player.objects.all().filter(is_active = True):
            if player.is_all_in:
                is_all_in_count += 1
        if is_all_in_count == num_active_players:
            return True
        fold_count = 0
        for player in Player.objects.all().filter(is_active = True):
            if player.most_recent_action == "fold":
                fold_count += 1
        if fold_count == num_active_players - 1:
            return True
        else:
            return False


    def isRoundOver(self, action):
        # action is a string that is passed in representing the action
        # action can be "call", "raise", "check", "fold"

        playersFolded = 0 
        for hand in Hand.objects.all():
            if not hand.is_active:
                playersFolded+=1 
    

        # activePlayers = Game.objects.first().players_connected - playersFolded
        num_active_players = Player.objects.all().filter(is_active = True).count()
        activePlayers = num_active_players - playersFolded
        
        # Everyone else has folded except 1 person, so round is over
        if activePlayers == 1 : 
            # game over is true, should do something
            return True

        # allActions has a list of all players actions (that have an active hand)
        allActions = [] 
        for hand in Hand.objects.all().filter(is_active=True):
            player_ID =  hand.player.id
            currPlayer = Player.objects.get(id=player_ID)
            allActions.append(currPlayer.most_recent_action)
        
        # check special edge cases if preflop 
        # big blind can check when everyone else has called but only pre-flop this is bc
        # they "opened" the betting so if the big bling is check and everyone else is call the round is also over 
        
        # 


    def playTurn(self, action): 
        # once a player makes a move (presses a button) this 
        # updates the game state to reflect their action
        # action is a string that is passed in representing the action
        # action can be "call", "raise", "check", "fold"
        currentGame = Game.objects.all().first()

        currRound = currentGame.curr_round
        currPlayer = currentGame.current_player.id
        maxBet = currentGame.highest_curr_bet

        print(action)
        print(f"Before Current Round: {currRound}")
        print(f"Before Current Player: {currPlayer}")
        print(f"Before Highest Curr Bet: {maxBet}")

        if (action == "call"):
            # maxBet stays the same
            print(Player.objects.all().filter(id=((currPlayer+1)%(currentGame.players_connected)))[0])
            call_action(currentGame, currentGame.current_player)
        elif action == "check":
            # check if it is legal 
            if (currRound==0):
                if currPlayer != currentGame.big_blind_player.id:
                    print("only big blind can check pre-flop!")
                else: 
                    check_action(currentGame, currentGame.current_player)
            elif (currRound > 0):
                if maxBet == 0: 
                    check_action(currentGame, currentGame.current_player)
                else: 
                    print("Can't check, opening bet has already been placed")

        elif action == "fold":
            for hand in Hand.objects.all():
                if hand.player.id == currPlayer.id:
                    updated_hand = hand
            fold_action(currentGame, currentGame.current_player, updated_hand)
        else: 
            validate = action.split(",")
            if len(validate) == 2 and validate[0] == "raise":
                try:
                    print(f"This the total pot before: {currentGame.total_pot}")
                    amount = int(validate[1])
                    # Valid raise action with a numeric amount
                    # You can handle the raise action here
                    currentGame.highest_curr_bet = amount
                    raise_action(currentGame.current_player, amount)
                except ValueError:
                    # Invalid amount (not a valid number after "raise,")
                    print("Invalid raise amount. Please provide a numeric value.")
            else:
                # Invalid format
                print("Invalid action format. Please use 'raise,x' format.")
        
        print(f"After Current Round: {currentGame.curr_round}")
        print(f"After Current Player: {currentGame.current_player.id}")
        print(f"After Highest Curr Bet: {currentGame.highest_curr_bet}")
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
    def gameInitalized(self): 
            community_cards = Game.objects.first().flop1 + "\n" + Game.objects.first().flop2 + "\n" + Game.objects.first().flop3 + "\n" +Game.objects.first().turn + "\n" + Game.objects.first().river
            print(community_cards)
            
            for hand in Hand.objects.all():
                print(f"This is {hand.player.user}'s hand: {hand.card_left} {hand.card_right}")
            
    def receive(self, **kwargs):
        if 'text_data' not in kwargs:
            self.send_error('you must send text_data')
            return

        try:
            data = json.loads(kwargs['text_data'])
        except json.JSONDecoder:
            self.send_error('invalid JSON sent to server')
            return

        if 'gameState' not in data:
            self.send_error('status property not sent in JSON')
            return
        
        if 'player_action' in data:
            player_action = data['player_action']
            print(player_action)

        status = data['gameState']
        active_players = 0 
        if(status=="ready"):
            for player in Player.objects.all():
                if player.is_active:
                    active_players+=1
            print(f" the number of players is: {active_players}")

            if (active_players >= 2 and Game.objects.count() == 0):
                print('game initiated')
                self.initGame()
            self.gameInitalized()
            print("before broadcast list")
            self.broadcast_list()
            return        

        # if (status == "start"):
        #         if (Game.objects.count() ==1):
        #             self.play() 
        #             return
        if (status == "inProgress") and (Game.objects.count() ==1):
                print("before PlayTurn")
                self.playTurn(player_action)
                print("after PlayTurn")
                self.isRoundOver(player_action)
        if (status == "finish"):
                self.finishGame(data)
                return

        else: self.send_error(f'Invalid status property: "{status}"')

    def broadcast_list(self):
        messages = {}
        # create the game info field in messages

        game_info = json.dumps(Game.make_game_list())
        
        messages['game_info'] = game_info
        messages['gameState'] = "inProgress"
        print(Player.make_active_player_list())
        active_players = json.dumps(Player.make_active_player_list())
        non_active_players = json.dumps(Player.make_non_active_player_list())
        messages['active_players_info'] = active_players
        messages['non_active_players_info'] = non_active_players
        print("inside broadcast list")

        async_to_sync(self.channel_layer.group_send)(
            self.group_name,
            {
                'type': 'broadcast_event',
                'message': json.dumps(messages)
            }
        )

    def broadcast_event(self, event):
        self.send(text_data=event['message'])