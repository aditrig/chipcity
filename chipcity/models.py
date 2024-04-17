from django.db import models
from django.contrib.auth.models import User
from django.conf import settings

'''
    This is the player model. Includes the user, user's wallet, seat number, profile picture, and is_active flag.
    References the game that it is in.
'''
class Player(models.Model):
    # bio = models.CharField(max_length=200)
    user = models.ForeignKey(User, on_delete=models.PROTECT, related_name="player",null=True) #associates each player with its corresponding user
    # game = models.ForeignKey(Game, on_delete=models.PROTECT, related_name="player_game",null=True) #associates each player with a specific game instance
    wallet = models.IntegerField(default=100,null=True) #associates each player with their own wallet (total amount of money they have)
    chips = models.IntegerField(default=50,null=True) #associates each player with their own number of chips (amount of money they bought in for)
    seat_number = models.IntegerField(default=0,null=True) #associates each player with their own specific seat # at the table
    # picture = models.FileField(blank=True,null=True) #associates each player with their own profile picture
    content_type = models.CharField(blank=True, max_length=50, null=True) #associates each player's profile picture with a corresponding content type
    is_participant = models.BooleanField(default=True) #checks if the player is an active player at the table (not spectator)
    is_big_blind = models.BooleanField(default=True)
    is_small_blind = models.BooleanField(default=True)
    is_all_in = models.BooleanField(default=False)
    current_bet = models.IntegerField(default=0,null=True)
    can_check = models.BooleanField(default=True)
    can_raise = models.BooleanField(default=True)
    can_call = models.BooleanField(default=True)
    most_recent_action = models.CharField(blank=True, max_length=50, null=True)
    card_left = models.CharField(max_length=20) #indicates the left card's suit and rank (ex: 6 of Hearts == 6H)
    card_right = models.CharField(max_length=20) #indicates the right card's suit and rank (ex: 6 of Hearts == 6H)
    hand_is_active = models.BooleanField(default=True) #indicates whether a player's hand is active (not folded)
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
                'wallet': player.wallet,
                'chips': player.chips,
                'seat_number': player.seat_number,
                # 'picture': player.picture,
                'content_type': player.content_type,
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
        print("we good?")

        return player_dict_lists
    
    @classmethod       
    def make_non_active_player_list(cls):
        player_dict_lists = []
        for player in cls.objects.all().filter(is_participant = False):
            player_dict = {
                'user': player.user.username,
                'wallet': player.wallet,
                'chips': player.chips,
                'seat_number': player.seat_number,
                # 'picture': player.picture,
                'content_type': player.content_type,
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
        print("we good?")

        return player_dict_lists

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
    big_blind_amt = models.IntegerField(default=2)
    small_blind_amt = models.IntegerField(default=1)
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
    @classmethod
    def make_game_list(cls):
        item_dict_list = []
        for item in cls.objects.all():
            item_dict = {
                'game_num': item.game_num,
                'players_connected': item.players_connected,
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
            }
            item_dict_list.append(item_dict)
        print(item_dict_list)
        return item_dict_list