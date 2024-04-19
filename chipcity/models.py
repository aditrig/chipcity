from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
from chipcity.card import *

'''
    This is the player model. Includes the user, user's wallet, seat number, profile picture, and is_active flag.
    References the game that it is in.
'''
class Player(models.Model):
    # bio = models.CharField(max_length=200)
    user = models.ForeignKey(User, on_delete=models.PROTECT, related_name="player",null=True) #associates each player with its corresponding user
    # game = models.ForeignKey(Game, on_delete=models.PROTECT, related_name="player_game",null=True) #associates each player with a specific game instance
    player_pressed_ready = models.BooleanField(default=True) #indicates if a player has pressed ready on the page (is_participant must be equal to True)
    wallet = models.IntegerField(default=100,null=True) #associates each player with their own wallet (total amount of money they have)
    chips = models.IntegerField(default=50,null=True) #associates each player with their own number of chips (amount of money they bought in for)
    seat_number = models.IntegerField(default=0,null=True) #associates each player with their own specific seat # at the table
    picture = models.CharField(blank=True, max_length=50, null=True) #associates each player with their own profile picture url
    # content_type = models.CharField(blank=True, max_length=50, null=True) #associates each player's profile picture with a corresponding content type
    is_participant = models.BooleanField(default=True) #checks if the player is an active player at the table (not spectator)
    is_big_blind = models.BooleanField(default=False)
    is_small_blind = models.BooleanField(default=False)
    is_all_in = models.BooleanField(default=False)
    current_bet = models.IntegerField(default=0,null=True)
    can_check = models.BooleanField(default=False)
    can_raise = models.BooleanField(default=True)
    can_call = models.BooleanField(default=True)
    most_recent_action = models.CharField(blank=True, max_length=50, null=True)
    card_left = models.IntegerField(default=0,null=True) #indicates the left card's suit and rank (ex: 6 of Hearts == 6H)
    card_right = models.IntegerField(default=0,null=True) #indicates the right card's suit and rank (ex: 6 of Hearts == 6H)
    hand_is_active = models.BooleanField(default=True) #indicates whether a player's hand is active (not folded)
    win_count = models.IntegerField(default=0,null=True)
    winning_hand = models.CharField(blank=True, max_length=50, null=True)
    # can_min = models.BooleanField(default=True)
    # can_half = models.BooleanField(default=True)
    # can_pot = models.BooleanField(default=True)
    # can_max = models.BooleanField(default=True)

    # def create_player(self, wallet, num_players, init_pot, curr_round):
    #     return type(self).objects.create(
    #     )
    # def __str__(self):
    #     return f"{self.user} is player number {self.id} in game {self.game}"
    @classmethod
    def make_active_player_list(cls):
        player_dict_lists = []
        for player in cls.objects.all().filter(is_participant = True):
            player_dict = {
                'user': player.user.username,
                'player_pressed_ready': player.player_pressed_ready,
                'wallet': player.wallet,
                'chips': player.chips,
                'seat_number': player.seat_number,
                'picture': player.picture,
                # 'content_type': player.content_type,
                'is_participant': player.is_participant,
                'is_big_blind': player.is_big_blind,
                'is_small_blind': player.is_small_blind,
                'is_all_in': player.is_all_in,
                'current_bet': player.current_bet,
                'can_check': player.can_check,
                'can_raise': player.can_raise,
                'can_call': player.can_call,
                'most_recent_action': player.most_recent_action,
                'card_left': player.card_left,
                'card_right': player.card_right,
                'hand_is_active': player.hand_is_active,
                'win_count': player.win_count,
                'winning_hand': player.winning_hand
            }
            player_dict_lists.append(player_dict)
        return player_dict_lists
    
    @classmethod       
    def make_non_active_player_list(cls):
        player_dict_lists = []
        for player in cls.objects.all().filter(is_participant = False):
            player_dict = {
                'user': player.user.username,
                'player_pressed_ready': player.player_pressed_ready,
                'wallet': player.wallet,
                'chips': player.chips,
                'seat_number': player.seat_number,
                'picture': player.picture,
                # 'content_type': player.content_type,
                'is_participant': player.is_participant,
                'is_big_blind': player.is_big_blind,
                'is_small_blind': player.is_small_blind,
                'is_all_in': player.is_all_in,
                'current_bet': player.current_bet,
                'can_check': player.can_check,
                'can_raise': player.can_raise,
                'can_call': player.can_call,
                'most_recent_action': player.most_recent_action,
                'card_left': player.card_left,
                'card_right': player.card_right,
                'hand_is_active': player.hand_is_active
            }
            player_dict_lists.append(player_dict)
        return player_dict_lists

'''
    This is the game class. Includes the game(table) number.
'''
class Game(models.Model):
    game_num = models.IntegerField(null=True) #indicates the game number (for our purposes should just be 1)
    players_connected = models.IntegerField(default=0) #indicates the number of players in the current game (including folded players)
    num_players_with_active_hand = models.IntegerField(default=0) #indicates the number of players who have an active hand
    list_of_active_players = models.CharField(blank=True, max_length=200, null=True)
    total_pot = models.IntegerField(default=0)
    flop1 = models.IntegerField(default=0)
    flop2 = models.IntegerField(default=0)
    flop3 = models.IntegerField(default=0)
    turn = models.IntegerField(default=0)
    river = models.IntegerField(default=0)
    curr_round = models.IntegerField(default=0)
    highest_curr_bet = models.IntegerField(default=0)
    last_raise = models.IntegerField(default=0)
    last_action =  models.IntegerField(default=0)
    big_blind_player = models.ForeignKey(Player, on_delete=models.PROTECT,related_name="big_blind_player", null=True)
    small_blind_player = models.ForeignKey(Player, on_delete=models.PROTECT,related_name="small_blind_player", null=True)
    big_blind_amt = models.IntegerField(default=2)
    small_blind_amt = models.IntegerField(default=1)
    current_player = models.ForeignKey(Player, on_delete=models.PROTECT,related_name="current_player", null=True)
    winning_player_user = models.CharField(blank=True, max_length=100, null=True)

    def create_game(self, game_num, num_players, init_pot, curr_round):
        return type(self).objects.create(
            game_num=game_num,
            players_connected=0,
            num_players_with_active_hand=0,
            total_pot=init_pot,
            flop1=None,
            flop2=None,
            flop3=None,
            turn=None,
            river=None,
            curr_round=curr_round # preflop, flop, turn, river from 0-3
        )
    # def __str__(self):
    #     return f"The game {self.id} is on round {self.curr_round} with {self.players_connected} players connected and the total pot at {self.total_pot}"
    @classmethod
    def make_game_list(cls):
        item_dict_list = []
        for item in cls.objects.all():
            item_dict = {
                'game_num': item.game_num,
                'players_connected': item.players_connected,
                'num_players_with_active_hand': item.num_players_with_active_hand,
                'list_of_active_players': item.list_of_active_players,
                'total_pot': item.total_pot,
                'flop1': item.flop1,
                'flop2': item.flop2,
                'flop3': item.flop3,
                'turn': item.turn,
                'river': item.river,
                'curr_round': item.curr_round,
                'highest_curr_bet': item.highest_curr_bet,
                'last_raise': item.last_raise,
                'last_action': item.last_action,
                'big_blind_player': item.big_blind_player.id,
                'small_blind_player': item.small_blind_player.id,
                'current_player_id': item.current_player.id,
                'current_player_user': item.current_player.user.username,
                'winning_player_user': item.winning_player_user
            }
            item_dict_list.append(item_dict)
        print(item_dict_list)
        return item_dict_list
    
    @classmethod
    def make_card_list(cls):
        card_dict_list = []
        card_dict = {
            'not-folded-back-art': "not-folded-back-art.svg",
            'folded-back-art': "folded-back-art.svg",
            str(Card.new('As')): "ace-of-spades.svg",
            str(Card.new('Ah')): "ace-of-hearts.svg",
            str(Card.new('Ad')): "ace-of-diamonds.svg",
            str(Card.new('Ac')): "ace-of-clubs.svg",
            str(Card.new('Ks')): "king-of-spades.svg",
            str(Card.new('Kh')): "king-of-hearts.svg",
            str(Card.new('Kd')): "king-of-diamonds.svg",
            str(Card.new('Kc')): "king-of-clubs.svg",
            str(Card.new('Qs')): "queen-of-spades.svg",
            str(Card.new('Qh')): "queen-of-hearts.svg",
            str(Card.new('Qd')): "queen-of-diamonds.svg",
            str(Card.new('Qc')): "queen-of-clubs.svg",
            str(Card.new('Js')): "jack-of-spades.svg",
            str(Card.new('Jh')): "jack-of-hearts.svg",
            str(Card.new('Jd')): "jack-of-diamonds.svg",
            str(Card.new('Jc')): "jack-of-clubs.svg",
            str(Card.new('Ts')): "ten-of-spades.svg",
            str(Card.new('Th')): "ten-of-hearts.svg",
            str(Card.new('Td')): "ten-of-diamonds.svg",
            str(Card.new('Tc')): "ten-of-clubs.svg",
            str(Card.new('9s')): "nine-of-spades.svg",
            str(Card.new('9h')): "nine-of-hearts.svg",
            str(Card.new('9d')): "nine-of-diamonds.svg",
            str(Card.new('9c')): "nine-of-clubs.svg",
            str(Card.new('8s')): "eight-of-spades.svg",
            str(Card.new('8h')): "eight-of-hearts.svg",
            str(Card.new('8d')): "eight-of-diamonds.svg",
            str(Card.new('8c')): "eight-of-clubs.svg",
            str(Card.new('7s')): "seven-of-spades.svg",
            str(Card.new('7h')): "seven-of-hearts.svg",
            str(Card.new('7d')): "seven-of-diamonds.svg",
            str(Card.new('7c')): "seven-of-clubs.svg",
            str(Card.new('6s')): "six-of-spades.svg",
            str(Card.new('6h')): "six-of-hearts.svg",
            str(Card.new('6d')): "six-of-diamonds.svg",
            str(Card.new('6c')): "six-of-clubs.svg",
            str(Card.new('5s')): "five-of-spades.svg",
            str(Card.new('5h')): "five-of-hearts.svg",
            str(Card.new('5d')): "five-of-diamonds.svg",
            str(Card.new('5c')): "five-of-clubs.svg",
            str(Card.new('4s')): "four-of-spades.svg",
            str(Card.new('4h')): "four-of-hearts.svg",
            str(Card.new('4d')): "four-of-diamonds.svg",
            str(Card.new('4c')): "four-of-clubs.svg",
            str(Card.new('3s')): "three-of-spades.svg",
            str(Card.new('3h')): "three-of-hearts.svg",
            str(Card.new('3d')): "three-of-diamonds.svg",
            str(Card.new('3c')): "three-of-clubs.svg",
            str(Card.new('2s')): "two-of-spades.svg",
            str(Card.new('2h')): "two-of-hearts.svg",
            str(Card.new('2d')): "two-of-diamonds.svg",
            str(Card.new('2c')): "two-of-clubs.svg"
        }
        card_dict_list.append(card_dict)
        return card_dict_list