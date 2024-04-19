from chipcity.models import *

def list_of_players():
    # Gets list of active players
    list = []
    for player in Player.objects.all():
        if player.is_participant:
            list.append(player)
    return list

def set_blinds(game):
    # Sets blinds for each round
    sb = ""
    bb = ""
    player_list = list_of_players()
    for player in player_list:
        if player.is_small_blind:
            sb = player
            bb = player_list[(player_list.index(player)+1)%(game.num_players_with_active_hand)]
        
    small_blind_player = sb
    big_blind_player = bb
    small_blind_player = bet_action(game, small_blind_player, game.small_blind_amt)
    big_blind_player = bet_action(game, big_blind_player, game.big_blind_amt)

    small_blind_player.save()
    big_blind_player.save()


def bet_action(game, player, money):
    # Bet functionality
    print(f"-----Now inside bet_action for {player.user}!-----")
    print(f"Is this Pre-Flop? (0-preflop, 1-flop, 2-turn, 3-river, 4-showdown): {game.curr_round}")
    print(f"If true, consider the following. If false, ignore...")
    print(f"---Is {player.user} the Small Blind?: {player.is_small_blind}")
    print(f"---If True, {player.user} should post {game.small_blind_amt}")
    print(f"---If False, ignore")
    print(f"---Is {player.user} the Big Blind?: {player.is_big_blind}")
    print(f"---If True, {player.user} should post {game.big_blind_amt}")
    print(f"---If False, ignore")
    print(f"Amount of Money {player.user} Posted: {money}")
    print(f"Before bet_action is run, {player.user}'s Chips: {player.chips}")
    print(f"Before bet_action is run, Total Pot Size: {game.total_pot}")
    print(f"True or False, {player.user} is All In?: {not (money < player.chips)}")
    if money < player.chips:
        player.current_bet += money
        player.chips -= money
        game.total_pot += money
    else:
        player.current_bet = player.chips
        player.chips = 0
        player.is_all_in = True

    print(f"After bet_action is run, {player.user}'s Chips: {player.chips}")
    print(f"After bet_action is run, Total Pot Size: {game.total_pot}")
    print(f"----------------------------------------------------")
    player.save()
    game.save()
    return player


def raise_action(player, money):
    # Raise functionality
    game = Game.objects.all().last()
    for otherplayer in Player.objects.all().filter(hand_is_active=True):
        if otherplayer.id != player.id:
            otherplayer.can_raise = True
            otherplayer.most_recent_action = "None"
            otherplayer.save()
        # if otherplayer.most_recent_action == "big blind":
        #     otherplayer.most_recent_action = "None"
        #     otherplayer.save()
    updated_player = bet_action(game, player, money)
    # game.current_player = Player.objects.all().filter(id=((updated_player.id)%(game.num_players_with_active_hand))+1)[0]
    updated_player.most_recent_action = "raise"
    updated_player.save()
    game.save()
    print(f"This the total pot after: {game.total_pot}")


def call_action(player):
    # Call functionality
    game = Game.objects.all().last()
    call_val = game.highest_curr_bet - player.current_bet
    print(f"Call Value: {call_val}")
    updated_player = bet_action(game, player, call_val)
    # game.current_player = Player.objects.all().filter(id=((updated_player.id)%(game.num_players_with_active_hand))+1)[0]
    updated_player.most_recent_action = "call"
    updated_player.save()
    game.save()
    print(f"This the total pot after: {game.total_pot}")


def all_in_action(game, player):
    # All in functionality
    player.current_bet += player.chips
    player.chips = 0
    player.is_all_in = True
    player.most_recent_action = "all in"
    game.total_pot += player.current_bet
    player.save()
    game.save()


def check_action(game, player):
    # Check functionality (doesn't do anything)
    # game.current_player = Player.objects.all().filter(id=((player.id)%(game.num_players_with_active_hand))+1)[0]
    player.most_recent_action = "check"
    player.save()
    game.save()


def fold_action(game, player):
    # Fold functionality
    player.hand_is_active = False
    player.current_bet = 0
    player.most_recent_action = "fold"
    # game.current_player = Player.objects.all().filter(id=((player.id)%(game.num_players_with_active_hand))+1)[0]
    player.save()


def allowed_action(game, player):
    # Tells which actions are allowed for each player
    player.can_check = can_check(game, player)
    player.can_call = can_call(game, player)
    player.can_raise = can_raise(game, player)
    player.can_fold = player.is_in_game
    player.can_all_in = player.is_in_game
    return player


def can_check(game, player):
    # Checks if player can check
    if game.highest_curr_bet <= player.current_bet:
        return True
    return False


def can_call(game, player):
    # Checks if player can call
    if (game.highest_curr_bet == 0):
        print("1")
        return False
    if (game.highest_curr_bet - player.current_bet) <= player.chips:
        print("2")
        return True
    elif (player.chips - game.highest_curr_bet) <= 0:
        print("3")
        player.is_all_in = True
        player.save()
        return True
    return False


def can_raise(game, player, amount):
    # Checks if player can raise
    print(f"Player's current bet: {player.current_bet}")
    if amount == 0 or amount <= game.highest_curr_bet:
        return False
    if (player.current_bet+amount) <= player.chips:
        return True
    return False


def reset_current_bets():
    # Resets the current bets for each player after a full round is finished
    player_list = list_of_players()
    for player in player_list:
        player.pot += player.current_bet
        player.current_bet = 0
        player.save()