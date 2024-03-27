from django.db import models
from django.contrib.auth.models import User
    

'''
    This is the game model. Includes the dealer, the number of players, the pot,
    the table number, and the small and big blinds.
'''
class Game(models.Model):
    dealer = models.ForeignKey(User, on_delete=models.PROTECT, related_name='dealer')
    num_of_players = models.IntegerField(default=2)
    pot = models.DecimalField(max_digits=10, decimal_places=2)
    table_num = models.ForeignKey(User, on_delete=models.PROTECT, related_name='table_num')
    small_blind = models.OneToOneField(User, on_delete=models.PROTECT, related_name="small_blind")
    big_blind = models.OneToOneField(User, on_delete=models.PROTECT, related_name="big_blind")

'''
    This is the player model. Includes the user, user's wallet, their hand, and profile picture.
'''
class Player(models.Model):
    # bio = models.CharField(max_length=200)
    user = models.OneToOneField(User, on_delete=models.PROTECT, related_name="player")
    game = models.ForeignKey(Game, on_delete=models.PROTECT, related_name="player_game")
    wallet = models.DecimalField(max_digits=6, decimal_places = 2)
    card_left = models.CharField(max_length=6)
    card_right = models.CharField(max_length=6)
    seat_number = models.IntegerField(default=0)
    picture = models.FileField(blank=True)
    content_type = models.CharField(blank=True, max_length=50)
    pot = models.IntegerField(default=0)

'''
    This is the card model. Includes the flop, turn, and river cards, the current player,
    the current player's bet, the pot, and the winner of the round.
'''
class Card(models.Model):
    game = models.ForeignKey(Game, on_delete=models.PROTECT, related_name="card_game")
    flop_left = models.CharField(max_length=6)
    flop_middle = models.CharField(max_length=6)
    flop_right = models.CharField(max_length=6)
    turn = models.CharField(max_length=6)
    river = models.CharField(max_length=6)
    players = models.ManyToManyField(Player)
    current_player = models.IntegerField(default=0)
    raise_amt = models.IntegerField(default=0)
    current_bet = models.IntegerField(default=0)
    player_pot = models.IntegerField(default=0)
    pot = models.IntegerField(default=0)
    winner = models.ManyToManyField(Player, related_name="winner")


