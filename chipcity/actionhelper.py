from chipcity.models import *

def list_of_players():
    # Gets list of active players
    list = []
    for player in Player.objects.all():
        if player.is_active:
            list.append(player)
    return list

def set_blinds(game, players):
    # Sets blinds for each round
    sb = ""
    bb = ""
    player_list = list_of_players()
    for player in player_list:
        if player.is_big_blind:
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
    player = bet_action(game, player, money)
    game = Game.objects.filter(id=player.game.id).first()
    player.save()
    game.save()


def call_action(game, player):
    # Call functionality
    call_val = player.round_bet - game.biggest_bet
    player = bet_action(player, call_val)
    # game = game_helper.new_bet(game, call_val, player.pot)
    player.save()
    game.save()


def all_in(game, player):
    """Bet all in.
    """
    player.round_bet += player.chips
    # game = game_helper.new_bet(game, player.chips, player.pot)
    player.chips = 0
    player.is_all_in = True
    player.save()
    game.save()


def check():
    """Check action.
    """
    return


def fold(player):
    """Fold action.

    :param player: [description]
    :type player: [type]
    """
    player.is_in_game = False
    player.save()


def set_allowed_actions(game, player):
    """Set actions which can player do this turn.

    :return: updated player object
    """
    player.can_check = can_check(game, player)
    player.can_call = can_call(game, player)
    player.can_raise = can_raise(game, player)
    player.can_fold = player.is_in_game
    player.can_all_in = player.is_in_game
    return player


def can_check(game, player):
    """Check if player can check.

    :return: bool
    """
    if game.biggest_bet <= player.round_bet:
        return True
    return False


def can_call(game, player):
    """Check if player can check.

    :return: bool
    """
    if (game.biggest_bet - player.pot) <= player.chips:
        return True
    return False


def can_raise(game, player):
    """Check if player can raise or reraise.

    Player can reraise only if someone else full raised.
    :return: bool
    """
    if (game.biggest_bet + game.last_raise - player.pot) <= player.chips:
        return True
    return False


def reset_round_bets(players):
    for player in players:
        player.pot += player.round_bet
        player.round_bet = 0
        player.save()