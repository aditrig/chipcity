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
            bb = player_list[(player_list.index(player)+1)%(game.players_connected)]
        
    small_blind_player = sb
    big_blind_player = bb
    small_blind_player = bet_action(small_blind_player, game.small_blind)
    big_blind_player = bet_action(big_blind_player, game.big_blind)

    small_blind_player.save()
    big_blind_player.save()


def bet_action(game, player, money):
    # Bet functionality
    if money < player.chips:
        player.chips -= money
        game.total_pot += money
    else:
        player.current_bet = player.chips
        player.chips = 0
        player.is_all_in = True
    return player


def raise_action(player, money):
    # Raise functionality
    game = Game.objects.all().first()
    updated_player = bet_action(game, player, money)
    game.current_player = Player.objects.all().filter(id=((updated_player.id)%(game.players_connected))+1)[0]
    updated_player.save()
    game.save()
    print(f"This the total pot after: {game.total_pot}")


def call_action(game, player):
    # Call functionality
    call_val = game.highest_curr_bet - player.current_bet
    updated_player = bet_action(game, player, call_val)
    game.current_player = Player.objects.all().filter(id=((updated_player.id)%(game.players_connected))+1)[0]
    player.save()
    game.save()


def all_in_action(game, player):
    # All in functionality
    player.current_bet += player.chips
    player.chips = 0
    player.is_all_in = True
    player.save()
    game.save()


def check_action(game, player):
    # Check functionality (doesn't do anything)
    game.current_player = Player.objects.all().filter(id=((player.id)%(game.players_connected))+1)[0]
    player.save()
    game.save()


def fold_action(game, player):
    # Fold functionality
    player.hand_is_active = False
    player.current_bet = 0
    game.current_player = Player.objects.all().filter(id=((player.id)%(game.players_connected))+1)[0]
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
    if (game.highest_curr_bet - player.current_bet) <= player.chips:
        return True
    return False


def can_raise(game, player):
    # Checks if player can raise
    if (game.highest_curr_bet + game.last_raise - player.current_bet) <= player.chips:
        return True
    return False


def reset_current_bets():
    # Resets the current bets for each player after a full round is finished
    player_list = list_of_players()
    for player in player_list:
        player.pot += player.current_bet
        player.current_bet = 0
        player.save()