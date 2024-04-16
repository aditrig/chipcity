from django.db import models
from django.contrib.auth.models import User
from django.conf import settings

'''
    This is the card model. Includes all the cards in a standard 52 card deck.
'''
SUIT_CHOICES = (
    ('c', 'Clubs'),
    ('d', 'Diamonds'),
    ('h', 'Hearts'),
    ('s', 'Spades'),
)

RANK_CHOICES = (
    ('2', '2'),
    ('3', '3'),
    ('4', '4'),
    ('5', '5'),
    ('6', '6'),
    ('7', '7'),
    ('8', '8'),
    ('9', '9'),
    ('T', 'Ten'),
    ('J', 'Jack'),
    ('Q', 'Queen'),
    ('K', 'King'),
    ('A', 'Ace'),
)

class StuffCard(models.Model):
    rank = models.CharField(max_length=5, choices=RANK_CHOICES, null=True)
    suit = models.CharField(max_length=10, choices=SUIT_CHOICES, null=True)

    def __str__(self):
        return f"{self.rank}{self.suit}"

'''
    This is the player model. Includes the user, user's wallet, seat number, profile picture, and is_active flag.
    References the game that it is in.
'''
class Player(models.Model):
    # bio = models.CharField(max_length=200)
    user = models.ForeignKey(User, on_delete=models.PROTECT, related_name="player",null=True) #associates each player with its corresponding user
    # game = models.ForeignKey(Game, on_delete=models.PROTECT, related_name="player_game",null=True) #associates each player with a specific game instance
    wallet = models.DecimalField(max_digits=6, decimal_places = 2,null=True) #associates each player with their own wallet (total amount of money they have)
    chips = models.DecimalField(max_digits=6, decimal_places = 2,null=True) #associates each player with their own number of chips (amount of money they bought in for)
    seat_number = models.IntegerField(default=0,null=True) #associates each player with their own specific seat # at the table
    picture = models.FileField(blank=True,null=True) #associates each player with their own profile picture
    content_type = models.CharField(blank=True, max_length=50, null=True) #associates each player's profile picture with a corresponding content type
    is_active = models.BooleanField(default=True) #checks if the player is an active player at the table (not spectator)
    is_big_blind = models.BooleanField(default=True)
    is_all_in = models.BooleanField(default=True)
    current_bet = models.IntegerField(default=0,null=True)
    can_check = models.BooleanField(default=True)
    can_raise = models.BooleanField(default=True)
    can_call = models.BooleanField(default=True)
    most_recent_action = models.CharField(blank=True, max_length=50, null=True)
    # can_min = models.BooleanField(default=True)
    # can_half = models.BooleanField(default=True)
    # can_pot = models.BooleanField(default=True)
    # can_max = models.BooleanField(default=True)

    # def create_player(self, wallet, num_players, init_pot, curr_round):
    #     return type(self).objects.create(
    #     )
    # def __str__(self):
    #     return f"{self.user} is player number {self.id} in game {self.game}"
    def make_active_player_list():
        player_dict_lists = []
        for player in cls.objects.all().filter(is_active = True):
            player_dict_lists = {
                'user': user,
                'game': game,
                'wallet': wallet,
                'chips': chips,
                'seat_number': seat_number,
                'picture': picture,
                'content_type': content_type,
                'is_active': is_active,
                'is_big_blind': is_big_blind,
                'is_all_in': is_all_in,
                'current_bet': current_bet,
                'can_check': can_check,
                'can_raise': can_raise,
                'can_call': can_call,
                'most_recent_action': most_recent_action
            }
    def make_non_active_player_list():
        player_dict_lists = []
        for player in cls.objects.all().filter(is_active = False):
            player_dict_lists = {
                'user': user,
                'game': game,
                'wallet': wallet,
                'chips': chips,
                'seat_number': seat_number,
                'picture': picture,
                'content_type': content_type,
                'is_active': is_active,
                'is_big_blind': is_big_blind,
                'is_all_in': is_all_in,
                'current_bet': current_bet,
                'can_check': can_check,
                'can_raise': can_raise,
                'can_call': can_call,
                'most_recent_action': most_recent_action
            }

'''
    This is the game model. Includes the game(table) number.
'''
class Game(models.Model):
    game_num = models.IntegerField(null=True) #indicates the game number (for our purposes should just be 1)
    players_connected = models.IntegerField(default=0)
    total_pot = models.IntegerField(default=0)
    flop1 = models.CharField(max_length=20, null=True)
    flop2 = models.CharField(max_length=20, null=True)
    flop3 = models.CharField(max_length=20, null=True)
    turn = models.CharField(max_length=20, null=True)
    river = models.CharField(max_length=20, null=True)
    curr_round = models.IntegerField(default=0)
    highest_curr_bet = models.IntegerField(default=0)
    last_raise = models.IntegerField(default=0)
    last_action =  models.IntegerField(default=0)
    big_blind_player = models.ForeignKey(Player, on_delete=models.PROTECT,related_name="big_blind_player", null=True)
    small_blind_player = models.ForeignKey(Player, on_delete=models.PROTECT,related_name="small_blind_player", null=True)
    current_player = models.ForeignKey(Player, on_delete=models.PROTECT,related_name="current_player", null=True)
    
    def create_game(self, game_num, num_players, init_pot, curr_round):
        return type(self).objects.create(
            game_num=game_num,
            players_connected=0,
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
    def make_game_list(cls):
        item_dict_list = []
        for item in cls.objects.all():
            item_dict = {
                'game_num': game_num,
                'players_connected': item.players_connected,
                'total_pot': item.total_pot,
                'flop1': flop1,
                'flop2': flop2,
                'flop3': flop3,
                'turn': turn,
                'river': river,
                'curr_round': item.curr_round,
                'highest_curr_bet': highest_curr_bet,
                'last_raise': last_raise,
                'last_action': last_action,
                'big_blind_player': big_blind_player,
                'small_blind_player': small_blind_player,
                'current_player': current_player
            }
            item_dict_list.append(item_dict)
        return item_dict_list
        

    
'''
    This is the hand model. Includes all each player's left and right cards (texas hold'em). Also checks if a hand is active (or in play).
    References the game that it is in and which player it is associated with.
'''
class Hand(models.Model):
    game = models.ForeignKey(Game, on_delete=models.PROTECT, related_name="hand_game") #associates a specific hand to the game instance it belongs to
    player = models.ForeignKey(Player, on_delete=models.PROTECT, related_name="card_player") #associates the hand dealt to a specific player
    card_left = models.CharField(max_length=10) #indicates the left card's suit and rank (ex: 6 of Hearts == 6H)
    card_right = models.CharField(max_length=10) #indicates the right card's suit and rank (ex: 6 of Hearts == 6H)
    is_active = models.BooleanField(default=True) #indicates whether a player's hand is active (not folded)

'''
    This is the round model. Includes whose turn it is and the round's current pot and highest bet.
    References the game that it is in and which player it is associated with.
'''
# class Round(models.Model):
#     game = models.ForeignKey(Game, on_delete=models.PROTECT, related_name="round_game") #associates each round with a specific game/table
#     current_player = models.ForeignKey(Player, on_delete=models.PROTECT, related_name='current_player') #indicates whose turn it is during each round
#     pot = models.IntegerField(default=0) #indicates the pot for each round
#     highest_bet = models.IntegerField(default=0) #indicates the highest bet placed per round
