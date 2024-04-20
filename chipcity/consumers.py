from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import async_to_sync
import json
from chipcity.models import Game, Player
from chipcity.views import * 
from chipcity.deck import *
from chipcity.actionhelper import *
from chipcity.evaluator import *
import random, math, requests

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
        if self.scope['user']:
            self.user = self.scope["user"]
            if (Game.objects.count() != 0 and Game.objects.last().curr_round<5):
                spectateMode = True
            else: 
                spectateMode = False
                print("New player has been created!")
            player, created = Player.objects.get_or_create(
                user=self.scope['user'],
                defaults={
                    'picture': self.scope['user'].social_auth.get(provider='google-oauth2').extra_data['picture'],
                    'is_participant': not spectateMode,  # This is only used if creating a new object
                    'hand_is_active': not spectateMode,
                    'spectator': spectateMode
                }
            )
            # print(player.user)
            # print(player.spectator)
            player.save()

        # If the player was not created, it means it already existed. In this case, only update is_active.
        if not created:  
            active_players = 0 
            for player in Player.objects.all():
                if player.is_participant:
                    active_players+=1

            player = Player.objects.get(user=self.user)
            if not player.spectator and active_players<6:
                player.is_participant = True
            # print(self.user)
            player.save()
            # if ((active_players) > 2):
                
            #     curr_game = Game.objects.last()
            #     curr_game.save()
            for player in Player.objects.all().filter(): 
                print(f"player: {player.user} spectator status: {player.spectator} and their participant status: {player.is_participant}")
        active_players = 0 
        for player in Player.objects.all():
            if player.is_participant:
                active_players+=1
        print(f"Number of Players That Are Participants: {active_players}")

        ready_players = 0
        for player in Player.objects.all().filter(player_pressed_ready=True):
            ready_players += 1
        
        print(f"The number of players pressed ready is: {ready_players}")
        
        self.user = self.scope["user"]
        self.broadcast_list()
        # self.send(text_data=json.dumps({"message": "i can say whatever i want"}))

        

    def disconnect(self, close_code):
        
        
        async_to_sync(self.channel_layer.group_discard)(
            self.group_name, self.channel_name
        )      
        print(self.user)
        
        player = Player.objects.get(user=self.user)
        if player== None: 
            return
        if player.spectator: 
            print(f"why r u disconnecting {player.user}")
            player.delete() 
            self.broadcast_list()
            return

            

        player.is_participant = False
        # player.player_pressed_ready = False
        player.hand_is_active = False
        if (Game.objects.last() and Game.objects.last().current_player == player): 
            self.playerTakeTurn("fold")
        player.save() 
        print("websocket is diconnected yay")
        for player in Player.objects.all().filter(): 
            print(f"player: {player.user} spectator status: {player.spectator} and their participant status: {player.is_participant}")

        active_players = 0 
        for player in Player.objects.all():
            if player.is_participant:
                active_players+=1

        print(f"number of active players: {active_players}")
        player = Player.objects.get(user=self.user)
            
        curr_game = Game.objects.last()
        if curr_game == None:
            return
        curr_game.players_connected = active_players
        curr_game.save()
        
        self.broadcast_list()
        

    def get_google_profile_picture(access_token):
        headers = {
            'Authorization': f'Bearer {access_token}'
        }
        response = requests.get('https://www.googleapis.com/oauth2/v2/userinfo', headers=headers)
        if response.status_code == 200:
            user_info = response.json()
            return user_info.get('picture')
        else:
            return None

    def isRoundOver(self, action):
        # action is a string that is passed in representing the action
        # action can be "call", "raise", "check", "fold"
        game = Game.objects.all().last()

        playersFolded = 0 
        for player in Player.objects.all():
            if not player.hand_is_active:
                playersFolded+=1 
        
        # activePlayers = Game.objects.last().players_connected - playersFolded
        num_players_with_active_hand = Player.objects.all().filter(hand_is_active = True).count()
        # activePlayers = num_active_players - playersFolded
    
        # Everyone else has folded except 1 person, so round and game is over
        # if num_players_with_active_hand == 1: 
        #     # game over is true, should do something
        #     print("Game is Over!")
        #     game.curr_round = 4
        #     game.save()
        #     self.resetRound()
        #     return True
        if self.isGameOver():
            game.curr_round = 5
            game.save()
            return True
        
        if self.isShowDown():
            game.curr_round = 4
            game.save()
            return True

        list_active_hand_players = []
        for player in Player.objects.all().filter(hand_is_active=True):
            list_active_hand_players.append(player)
        print(f"list_active_hand_players: {list_active_hand_players}")
        print(f"game.players_connected: {game.players_connected}")
        
        list_are_participants = []
        for player in Player.objects.all().filter(is_participant=True):
            list_are_participants.append(player)

        print(f"list_are_participants: {list_are_participants}")

        current_player = game.current_player
        print(f"This is current player: {game.current_player.user}")
        
        num_players_at_start = 0
        for player in Player.objects.all().filter(player_pressed_ready = True):
            num_players_at_start += 1
        
        print(f"PLAYERS AT START:{num_players_at_start}")
        # Checks for the player to the left of the current player's existance in list_active_hand_players
        firstPlayer = Player.objects.all().filter(id=((game.big_blind_player.id)%(num_players_at_start))+1)[0]
        if firstPlayer in list_active_hand_players:
            current_player = firstPlayer
        elif game.big_blind_player in list_active_hand_players:
            currPlay = Player.objects.all().filter(id=((game.big_blind_player.id)%(num_players_at_start))+1)[0]
            count = 1
            while currPlay not in list_active_hand_players or currPlay.is_all_in:
                print(f"PLAYERS CONNECTED INSIDE 1: {num_players_at_start}")
                currPlay = Player.objects.all().filter(id=((game.big_blind_player.id+count)%(num_players_at_start))+1)[0]
                count += 1
            current_player = currPlay
        elif game.small_blind_player in list_active_hand_players:
            currPlay = Player.objects.all().filter(id=((game.small_blind_player.id)%(num_players_at_start))+1)[0]
            count = 1
            while currPlay not in list_active_hand_players or currPlay.is_all_in:
                print(f"PLAYERS CONNECTED INSIDE 2: {num_players_at_start}")
                currPlay = Player.objects.all().filter(id=((game.small_blind_player.id+count)%(num_players_at_start))+1)[0]
                count += 1
            current_player = currPlay
        # elif game.big_blind_player not in list_active_hand_players and game.small_blind_player in list_active_hand_players:
        #     current_player = Player.objects.all().filter(id=((game.small_blind_player.id)%(game.players_connected))+1)[0]
        elif Player.objects.all().filter(id=((game.current_player.id)%(num_players_at_start))+1)[0] in list_active_hand_players and not Player.objects.all().filter(id=((game.current_player.id)%(num_players_at_start))+1)[0].is_all_in:
            print(f"PLAYERS CONNECTED INSIDE 3: {num_players_at_start}")
            current_player = Player.objects.all().filter(id=((game.current_player.id)%(num_players_at_start))+1)[0]
        else: # If doesn't exist, finds next closest player
            print(f"PLAYERS CONNECTED INSIDE 4: {num_players_at_start}")
            currPlay = Player.objects.all().filter(id=((game.current_player.id)%(num_players_at_start))+1)[0]
            count = 1
            while currPlay not in list_active_hand_players or currPlay.is_all_in:
                currPlay = Player.objects.all().filter(id=((game.current_player.id+count)%(num_players_at_start))+1)[0]
                count += 1
            current_player = currPlay
                            
        # allActions has a list of all players actions (that have an active hand)
        allActions = [] 
        all_in_count = 0
        for player in Player.objects.all().filter(hand_is_active=True):
            if player.is_all_in:
                all_in_count += 1
            player_ID =  player.id
            currPlayer = Player.objects.get(id=player_ID)
            allActions.append(currPlayer.most_recent_action)
        
        # If only 2 people left and one of them is all in, go straight to ShowDown (Round Over = True)
        if len(list_active_hand_players) == 2 and all_in_count == 1:
            print("Round is Over!")
            game.curr_round = 4
            game.current_player = current_player
            game.save()
            self.resetRound()
            return True
        
        # check special edge cases if preflop 
        # big blind can check when everyone else has called but only pre-flop this is bc
        # they "opened" the betting so if the big blind is check and everyone else is call the round is also over 
        if action == "check" and (Game.objects.last().curr_round == 0) and (allActions.count("call") == (num_players_with_active_hand - 1)) and  (Game.objects.last().current_player == Game.objects.last().big_blind_player):
            print("Round is Over!")
            game.curr_round += 1
            game.current_player = current_player
            game.save()
            self.resetRound()
            return True
        if action == "check" and (Game.objects.last().curr_round > 0) and (allActions.count("check") == (num_players_with_active_hand)):
            print("Round is Over!")
            game.curr_round += 1
            game.current_player = current_player
            game.save()
            self.resetRound()
            return True
        # checks only one person has raised and all others have called
        elif "raise" in allActions and (allActions.count("call") == num_players_with_active_hand - 1):
            allAmounts = []
            for player in Player.objects.all().filter(hand_is_active=True):
                allAmounts.append(player.current_bet)
            if len(set(allAmounts)) == 1:
                print("Round is Over!")
                game.curr_round += 1
                game.current_player = current_player
                game.save()
                self.resetRound()
                return True
        # checks only one person has raised and all others have called minus person all in (must have at least one all in)
        elif "raise" in allActions and (allActions.count("call") == num_players_with_active_hand - all_in_count - 1):
            if allActions.count("all in") > 0:
                print("Round is Over!")
                game.curr_round += 1
                game.current_player = current_player
                game.save()
                self.resetRound()
                return True
        # everyone checks
        elif (allActions.count("check") == num_players_with_active_hand - all_in_count):
            print("Round is Over!")
            game.curr_round += 1
            game.current_player = current_player
            game.save()
            self.resetRound()
            return True
        

        print("Round is not Over!")
        print(((game.current_player.id)%(num_players_at_start))+1)
        if Player.objects.all().filter(id=((game.current_player.id)%(num_players_at_start))+1)[0] in list_active_hand_players and not Player.objects.all().filter(id=((game.current_player.id)%(num_players_at_start))+1)[0].is_all_in:
            game.current_player = Player.objects.all().filter(id=((game.current_player.id)%(num_players_at_start))+1)[0]
            game.current_player.save()
            game.save()
        else:
            currPlay = Player.objects.all().filter(id=((game.current_player.id)%(num_players_at_start))+1)[0]
            count = 1
            while currPlay not in list_active_hand_players or currPlay.is_all_in:
                currPlay = Player.objects.all().filter(id=((game.current_player.id+count)%(num_players_at_start))+1)[0]
                count += 1
            game.current_player = currPlay
            game.current_player.save()
            game.save()
        print(f"This is now the current player: {game.current_player.user}")
        return False

    def isShowDown(self):
        game = Game.objects.last()
        print(f"Game's Current Round: {game.curr_round}")
        if game.curr_round == 4:
            # showdown
            print("Showdown!")
            game.curr_round = 5
            game.save()
            return True
        num_players_with_active_hand = Player.objects.all().filter(hand_is_active = True).count()
        
        # Checks if every active hand player is all in
        is_all_in_count = 0
        for player in Player.objects.all().filter(hand_is_active = True):
            if player.is_all_in:
                is_all_in_count += 1
        if ((num_players_with_active_hand - is_all_in_count) == 1):
            print("Showdown!")
            game.curr_round = 5
            game.save()
            return True

        if is_all_in_count == num_players_with_active_hand:
            print("Showdown!")
            game.curr_round = 5
            game.save()
            return True
        return False
        
    def isGameOver(self):
        game = Game.objects.last()
        if game.curr_round == 5:
            print("Game Over!")
            return True
        num_players_with_active_hand = Player.objects.all().filter(hand_is_active = True).count()
        # Checks if only one active hand player
        active_hand_count = 0
        for player in Player.objects.all().filter(hand_is_active = True):
            active_hand_count += 1
        if active_hand_count == 1:
            print("Game is Over!")
            return True
        # Checks if everyone has folded except one player
        fold_count = 0
        for player in Player.objects.all().filter(hand_is_active = True):
            if player.most_recent_action == "fold":
                fold_count += 1
        if fold_count == num_players_with_active_hand - 1:
            print("Game is Over!")
            return True
        else:
            return False
        
    def evaluateHands(self):
        game = Game.objects.last()
        list_of_players_with_active_hand = []
        for player in Player.objects.all().filter(hand_is_active = True):
            list_of_players_with_active_hand.append(player)
        print(list_of_players_with_active_hand)
        
        list_of_hands = []
        for player in Player.objects.all().filter(hand_is_active = True):
            hand = [player.card_left, player.card_right]
            list_of_hands.append(hand)
        print(list_of_hands)
        evaluator = Evaluator()
        board = [game.flop1, game.flop2, game.flop3, game.turn, game.river]
        print(f"This is the Board: {board}")
        print(f"This is the list_of_hands that need to evaluated: {list_of_hands}")
        winner = evaluator.hand_summary(board, list_of_hands)
        print(f"This is the evaluator summary to find winner")
        if len(winner) == 1:
            # print(f"{list_of_players_with_active_hand[winner[0][0]].user} won with a {winner[0][1]}")
            for player in Player.objects.all().filter(hand_is_active = True):
                if player.id == list_of_players_with_active_hand[winner[0][0]].id:
                    player.win_count += 1
                    player.winning_hand = winner[0][1]
                    # Give Rewards
                    player.chips += game.total_pot
                    player.save()
                    game.winning_player_user = f"{list_of_players_with_active_hand[winner[0][0]].user} won with a {winner[0][1]}"
                    game.save()
        else:
            winning_player_user_list = []
            for i in range(len(winner)):
                print(f"{list_of_players_with_active_hand[winner[i][0]].user},")
                print(f"Split Pot with a {winner[0][1]}")
                win = list_of_players_with_active_hand[winner[i][0]]
                win.win_count += 1
                win.winning_hand = winner[0][1]
                win.chips += math.ceil(game.total_pot/len(winner))
                win.save()
                winning_player_user_list.append(win.user.username)
            concatenated_winners = ", ".join(winning_player_user_list)
            concatenated_winners += f" split pot with a {winner[0][1]}"
            game.winning_player_user = concatenated_winners
            game.save()
    
    def resetRound(self):
        game = Game.objects.all().last()
        game.highest_curr_bet = 0
        for player in Player.objects.all().filter(hand_is_active=True):
            player.current_bet = 0
            player.most_recent_action = "NULL"
            player.save()
        game.save()

    def playTurn(self, action): 
        # once a player makes a move (presses a button) this 
        # updates the game state to reflect their action
        # action is a string that is passed in representing the action
        # action can be "call", "raise", "check", "fold"
        currentGame = Game.objects.all().last()

        currRound = currentGame.curr_round

        print(f"This is the Current Player: {currentGame.current_player.user}")
        print(f"This is {currentGame.current_player.user}'s action: {action}")
        print(f"This is the Current Round (0-preflop, 1-flop, 2-turn, 3-river, 4-showdown): {currRound}")
        print(f"Before any turn is computed, this is the Current Round's Highest Current Bet: {currentGame.highest_curr_bet}")
        
        if (action == "call"):
            # maxBet stays the same
            if (can_call(currentGame, currentGame.current_player) and currentGame.current_player.most_recent_action != "big blind"):
                if currentGame.current_player.is_all_in:
                    print("all in!")
                    all_in_action(currentGame, currentGame.current_player)
                    currentGame.current_player.can_call = True
                    currentGame.current_player.save()
                    action = "all in"
                else:
                    call_action(currentGame.current_player)
                    currentGame.current_player.can_call = True
                    currentGame.current_player.save()
            else:
                print("Calling is not a legal action!")
                currentGame.current_player.can_call = False
                currentGame.current_player.save()
                return False
        elif action == "check":
            # check if it is legal 
            if (currRound==0):
                if currentGame.current_player.id != currentGame.big_blind_player.id and not can_check(currentGame, currentGame.current_player):
                    print("only big blind can check pre-flop!")
                    currentGame.current_player.can_check = False
                    currentGame.current_player.save()
                    return False
                elif currentGame.current_player.id == currentGame.big_blind_player.id and not can_check(currentGame, currentGame.current_player):
                    print("Can't check, opening bet has already been placed")
                    currentGame.current_player.can_check = False
                    currentGame.current_player.save()
                    return False
                else: 
                    check_action(currentGame, currentGame.current_player)
                    currentGame.current_player.can_check = True
                    currentGame.current_player.save()
            elif (currRound > 0):
                if can_check(currentGame, currentGame.current_player) or currentGame.highest_curr_bet == 0: 
                    check_action(currentGame, currentGame.current_player)
                    currentGame.current_player.can_check = True
                    currentGame.current_player.save()
                else: 
                    print("Can't check, opening bet has already been placed")
                    currentGame.current_player.can_check = False
                    currentGame.current_player.save()
                    return False

        elif action == "fold":
            fold_action(currentGame, currentGame.current_player)
            currentGame.num_players_with_active_hand -= 1
            currentGame.save()
        else: 
            validate = action.split(",")
            if len(validate) == 2 and validate[0] == "raise":
                try:
                    amount = int(validate[1])
                    print(f"Raise amount: {amount}")
                    if can_raise(currentGame, currentGame.current_player, amount):
                        print(f"This the total pot before: {currentGame.total_pot}")
                        # Valid raise action with a numeric amount
                        # You can handle the raise action here
                        currentGame.highest_curr_bet = currentGame.current_player.current_bet + amount
                        currentGame.save()
                        raise_action(currentGame.current_player, amount)
                        currentGame.current_player.can_raise = False
                        currentGame.current_player.save()
                    else:
                        print("Cannot raise by zero, cannot raise less than or equal to highest current bet, or have insufficient funds!")
                        currentGame.current_player.can_raise = False
                        currentGame.current_player.save()
                        return False
                except ValueError:
                    # Invalid amount (not a valid number after "raise,")
                    print("Invalid raise amount. Please provide a numeric value.")
                    return False
            else:
                # Invalid format
                print("Invalid action format. Please use 'raise,x' format.")
                return False
        
        # currentGame.save()
        # currentGame.current_player.save()
        print(f"This is the Current Player: {currentGame.current_player.user}")
        print(f"This is {currentGame.current_player.user}'s action: {action}")
        print(f"This is the Current Round (0-preflop, 1-flop, 2-turn, 3-river, 4-showdown): {currentGame.curr_round}")
        print(f"After turn is computed, this is the Current Round's Highest Current Bet: {currentGame.highest_curr_bet}")
        print(f"After turn is computed, this is the Current Player's Current Bet: {currentGame.current_player.current_bet}")
        # currentGame.current_player = Player.objects.all().filter(id=((currentGame.current_player.id)%(currentGame.num_players_with_active_hand))+1)[0]
        # currentGame.current_player.save()
        # currentGame.save()
        return True
        
        # want it so that when one player is disconnected, set their active status to false
    
    def initGame(self):
        print(f"Game object count: {Game.objects.count()}")
        active_players = 0 
        for player in Player.objects.all():
            if player.is_participant:
                active_players+=1
        print(f"I am now inside initGame() with the number of active players: {active_players}")

        if active_players < 2:
            # Makes sure that game does not start without 2+ players
            return
        
        # Gets list of active players
        list_of_active_players = list_of_players()
        print(f"Printing list of active player objects!: {list_of_active_players}")

        list = []
        for player in Player.objects.all():
            if player.is_participant:
                list.append(player.user.username)
                player.player_pressed_ready = True
                player.save() 


        Game_Action.start_new_game(self,1,active_players)
        # Sets BBP and SBP
        curr_game = Game.objects.last()
        curr_game.list_of_active_players = str(list)
        print(curr_game)
        curr_game.small_blind_player = list_of_active_players[0]
        curr_game.big_blind_player = list_of_active_players[1]
        # curr_game.big_blind_player.most_recent_action = "raise"
        # curr_game.big_blind_player.can_check = True
        # curr_game.big_blind_player.save()
        curr_game.current_player = list_of_active_players[(list_of_active_players.index(curr_game.big_blind_player)+1)%(curr_game.players_connected)]
        print(f"The Small Blind Player is: {curr_game.small_blind_player.user}")
        print(f"The Big Blind Player is: {curr_game.big_blind_player.user}")
        print(f"The Current Player is: {curr_game.current_player.user}")
        curr_game.save()

        for player in Player.objects.all().filter(is_participant=True):
            if player.id == curr_game.big_blind_player.id:
                player.is_big_blind = True
                player.is_small_blind = False
                player.can_check = True
                player.most_recent_action = "big blind"
            elif player.id == curr_game.small_blind_player.id:
                player.is_small_blind = True
                player.is_big_blind = False
            else:
                player.is_small_blind = False
                player.is_big_blind = False
            player.save()
        
        updated_game = Game.objects.last()
        updated_game.highest_curr_bet = updated_game.big_blind_amt
        updated_game.small_blind_player = bet_action(updated_game, updated_game.small_blind_player, updated_game.small_blind_amt)
        updated_game.big_blind_player = bet_action(updated_game, updated_game.big_blind_player, updated_game.big_blind_amt)
        updated_game.small_blind_player.save()
        updated_game.big_blind_player.save()
        updated_game.save()

        for player in Player.objects.all().filter(is_participant=True):
            print(f"This is {player.user}'s hand: {player.card_left} {player.card_right}")

        number_of_players_with_active_hand = 0
        for player in Player.objects.all().filter(hand_is_active=True):
            number_of_players_with_active_hand += 1
        
        updated_game.num_players_with_active_hand = number_of_players_with_active_hand
        updated_game.save()

        # print("-----This is the board:-----")
        # print(response)

        # self.send(text_data=json.dumps({"message": response }))
    def gameInitalized(self): 
            game = Game.objects.last()
            print("-----This is the board:-----")
            print(Card.int_to_pretty_str(game.flop1))
            print(Card.int_to_pretty_str(game.flop2))
            print(Card.int_to_pretty_str(game.flop3))
            print(Card.int_to_pretty_str(game.turn))
            print(Card.int_to_pretty_str(game.river))
            print("----------------------------")
            # for player in Player.objects.all():
            #     print(f"This is {player.user}'s hand: {Card.int_to_pretty_str(player.card_left)} {Card.int_to_pretty_str(player.card_right)}")

    def newGame(self):
        print(f"Game object count: {Game.objects.count()}")
        active_players = 0 
        for player in Player.objects.all():
            if player.is_participant:
                active_players+=1
        print(f"I am now inside initGame() with the number of active players: {active_players}")

        if active_players < 2:
            # Makes sure that game does not start without 2+ players
            self.close()
            return

        spectatorCount = 0 
        spectatorList =[] 
        
        for player in Player.objects.all(): 
            print(f"player: {player.user} spectator status: {player.spectator} and their participant status: {player.is_participant}")
            if player.spectator:
                spectatorCount+=1
                spectatorList.append(player)
        print(spectatorList)
            
        
        if active_players < 3: 
            print("active_players less than 3")
            for i in range(min(len(spectatorList), 3 - active_players)):
                specToPlayer = spectatorList[i]
                specToPlayer.spectator = False
                specToPlayer.is_participant = True
                print(f"this is the spectator: {specToPlayer.user}, who has become an active player")
                specToPlayer.save()        
            
            for player in Player.objects.all():
                if not player.is_participant:
                    player.spectator = True
                    print(player.user)
                    player.save()
        
        # Gets list of active players
        list_of_active_players = list_of_players()
        
        # Moves players to the back, essentially "simulating" changing of blinds
        # Number of times to rotate
        num = Game.objects.count() % len(list_of_active_players)
        list_of_active_players = list_of_active_players[num:] + list_of_active_players[:num]
        
        list = []
        for player in list_of_active_players:
            player.save() 
            list.append(player.user.username)

        Game_Action.start_new_game(self,1,active_players)
        # Sets BBP and SBP
        curr_game = Game.objects.last()
        print(curr_game)
        curr_game.small_blind_player = list_of_active_players[0]
        curr_game.big_blind_player = list_of_active_players[1]
        curr_game.current_player = list_of_active_players[(list_of_active_players.index(curr_game.big_blind_player)+1)%(curr_game.players_connected)]
        print(f"The Small Blind Player is: {curr_game.small_blind_player.user}")
        print(f"The Big Blind Player is: {curr_game.big_blind_player.user}")
        print(f"The Current Player is: {curr_game.current_player.user}")
        curr_game.game_num = Game.objects.all().count()
        curr_game.players_connected = active_players
        curr_game.num_players_with_active_hand = active_players
        curr_game.list_of_active_players = str(list)
        curr_game.save()

        for player in Player.objects.all().filter(is_participant=True):
            player.is_participant = True
            player.is_all_in = False
            player.current_bet = 0
            player.can_check = False
            player.can_raise = True
            player.can_call = True
            player.most_recent_action = "NULL"
            player.hand_is_active = True
            if player.id == curr_game.big_blind_player.id:
                player.is_big_blind = True
                player.is_small_blind = False
                player.can_check = True
                player.most_recent_action = "big blind"
            elif player.id == curr_game.small_blind_player.id:
                player.is_small_blind = True
                player.is_big_blind = False
            else:
                player.is_small_blind = False
                player.is_big_blind = False
            player.save()
        
        updated_game = Game.objects.last()
        updated_game.highest_curr_bet = updated_game.big_blind_amt
        updated_game.total_pot = 0
        updated_game.small_blind_player = bet_action(updated_game, updated_game.small_blind_player, updated_game.small_blind_amt)
        updated_game.big_blind_player = bet_action(updated_game, updated_game.big_blind_player, updated_game.big_blind_amt)
        updated_game.small_blind_player.save()
        updated_game.big_blind_player.save()
        updated_game.save()

        for player in Player.objects.all().filter(is_participant=True):
            print(f"This is {player.user}'s hand: {player.card_left} {player.card_right}")

        number_of_players_with_active_hand = 0
        for player in Player.objects.all().filter(hand_is_active=True):
            number_of_players_with_active_hand += 1
        
        updated_game.num_players_with_active_hand = number_of_players_with_active_hand
        updated_game.save()

        # print("-----This is the board:-----")
        # print(response)

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

        if 'gameState' not in data:
            self.send_error('status property not sent in JSON')
            return
        
        if 'player_action' in data:
            player_action = data['player_action']
            # print(player_action)

        print(f"data dump: {data}")
        status = data['gameState']
        active_and_ready_players = 0 
        num_participants = 0
        if(status=="ready"):
            user_readied = data['user_pressed_ready']
            for player in Player.objects.all():
                if player.is_participant:
                    num_participants += 1
            for player in Player.objects.all():
                if player.user.username == user_readied:
                    player.player_pressed_ready = True
                    player.save()
            for player in Player.objects.all():
                if player.is_participant and player.player_pressed_ready:
                    active_and_ready_players+=1
            print("")
            print("-----Pressed Ready! Currently in Ready State!-----")
            print(f"The number active AND ready players is: {active_and_ready_players}")
            print("")

            if (num_participants != active_and_ready_players):
                print("Waiting for players to ready up!")

            else:
                if (active_and_ready_players < 2):
                    print("Cannot Start Game With Less Than Two Players!")
                    return

                if (active_and_ready_players >= 2 and Game.objects.count() == 0):
                    print("-----Game Initiated! Entering initGame()-----")
                    self.initGame()
                    print("-----Exiting initGame()-----")
                    print("")
                    print("-----Entering gameInitalized()-----")
                    self.gameInitalized()
                    print("-----Exiting gameInitalized()-----")
                    print("")
                    print("-----Entering broadcast_list()!-----")
                    self.broadcast_list()    
                    print("-----Exiting broadcast_list()!-----") 
                    return
                elif (Game.objects.last().curr_round==5): 
                        print("-----Starting New Game! Entering newGame()!-----")
                        self.newGame()
                        print("-----Exiting newGame()!-----")
                        print("")
                        print("-----Entering broadcast_list()!-----")
                        self.broadcast_list()
                        print("-----Exiting broadcast_list()!-----")
                        print("")
                        return
                # game got interuptted 
                elif (Game.objects.last().winning_player_user == None):
                        print("-----Starting New Game! Entering newGame()!-----")
                        self.newGame()
                        print("-----Exiting newGame()!-----")
                        print("")
                        print("-----Entering broadcast_list()!-----")
                        self.broadcast_list()
                        print("-----Exiting broadcast_list()!-----")
                        print("")
                        return
        if (status == "newGame"):
            user_readied = data['user_pressed_ready']
            for player in Player.objects.all():
                if player.user.username == user_readied:
                    player.player_pressed_ready = True
                    player.save()
            for player in Player.objects.all():
                if player.is_participant and player.player_pressed_ready:
                    active_and_ready_players+=1
            print("")
            print("-----New Game! Currently in newGame State!-----")
            print(f"The number of players is: {active_and_ready_players}")
            print("")
            
            user_readied = data['user_pressed_ready']
            num_participants = Player.objects.filter(is_participant=True).count()
            ready_players = Player.objects.filter(user__username=user_readied, is_participant=True)
            
            for player in ready_players:
                player.player_pressed_ready = True
                player.save()
    
            active_and_ready_players = Player.objects.filter(is_participant=True, player_pressed_ready=True).count()
            print("")
            print("-----Pressed Ready! Currently in Ready State!-----")
            print(f"The number active AND ready players is: {active_and_ready_players}")
            print("")

            if num_participants != active_and_ready_players:
                print("Waiting for players to ready up!")
            

            if (active_and_ready_players < 2):
                print("Cannot Start Game With Less Than Two Players!")

            if (active_and_ready_players >= 2 and Game.objects.count() == 0):
                print("-----Game Initiated! Entering initGame()-----")
                self.initGame()
                print("-----Exiting initGame()-----")
            print("")
            print("-----Entering gameInitalized()-----")
            self.gameInitalized()
            print("-----Exiting gameInitalized()-----")
            print("")
            print("-----Entering broadcast_list()!-----")
            self.broadcast_list()    
            print("-----Exiting broadcast_list()!-----") 
            
        if status == "inProgress":
            self.playerTakeTurn(player_action)
        else: 
            self.send_error(f'Invalid status property: "{status}"')
        
    def playerTakeTurn(self, player_action):
        if self.playTurn(player_action):
            print("-----Exiting playTurn()!-----")
            print("")
            print("-----Entering isRoundOver()!-----")
            self.isRoundOver(player_action)
            print("-----Exiting isRoundOver()!-----")
            print("")
            print("-----Entering isShowDown()!-----")
            if self.isShowDown():
                print("-----is showdown going to broadcast list!-----")
                self.broadcast_list()
                print("-----Exiting isShowDown()!-----")
                print("")
                print("-----Entering isGameOver()!-----")
                if self.isGameOver():
                    self.evaluateHands()
            print("-----Exiting isGameOver()!-----")
            print("")
            print("-----Entering broadcast_list()!-----")
            self.broadcast_list()
            print("-----Exiting broadcast_list()!-----")
            print("")
            if Game.objects.last().curr_round == 5:
                print("Finished Game!")
                print("Inside Finish, need to reset everything!")
                # self.finishGame(data)
                print(Game.objects.last().curr_round)
                print("going to broadcast list")
                status = "finish"
                for player in Player.objects.all().filter(is_participant=True):
                    player.player_pressed_ready = False
                    player.save()

                self.broadcast_list()
                print("exiting broadcast lsit")

                status = "ready"
        else:
            print(Game.objects.last().current_player)




    def broadcast_list(self):
        messages = {}
        # create the game info field in messages

        game_info = json.dumps(Game.make_game_list())
        
        messages['game_info'] = game_info
        messages['gameState'] = "inProgress"
        messages['cards'] = json.dumps(Game.make_card_list())
        # print(Player.make_active_player_list())
        active_players = json.dumps(Player.make_active_player_list())
        non_active_players = json.dumps(Player.make_non_active_player_list())
        messages['active_players_info'] = active_players
        messages['non_active_players_info'] = non_active_players
        async_to_sync(self.channel_layer.group_send)(
            self.group_name,
            {
                'type': 'broadcast_event',
                'message': json.dumps(messages)
            }
        )

    def broadcast_event(self, event):
        self.send(text_data=event['message'])