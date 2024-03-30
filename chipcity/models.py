from django.db import models
from django.contrib.auth.models import User

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

class Card(models.Model):
    rank = models.CharField(max_length=5, choices=RANK_CHOICES, null=True)
    suit = models.CharField(max_length=10, choices=SUIT_CHOICES, null=True)

    def __str__(self):
        return f"{self.rank}{self.suit}"

'''
    This is the game model. Includes the game(table) number.
'''
class Game(models.Model):
    game_num = models.IntegerField(null=True) #indicates the game number (for our purposes should just be 1)
    players_connected = models.IntegerField(default=0)
    total_pot = models.IntegerField(default=0)
    flop1 = models.ForeignKey(Card, on_delete=models.CASCADE, related_name='flop1', blank=True, null=True)
    flop2 = models.ForeignKey(Card, on_delete=models.CASCADE, related_name='flop2', blank=True, null=True)
    flop3 = models.ForeignKey(Card, on_delete=models.CASCADE, related_name='flop3', blank=True, null=True)
    turn = models.ForeignKey(Card, on_delete=models.CASCADE, related_name='turn', blank=True, null=True)
    river = models.ForeignKey(Card, on_delete=models.CASCADE, related_name='river', blank=True, null=True)
    curr_round = models.IntegerField(default=0)


'''
    This is the player model. Includes the user, user's wallet, seat number, profile picture, and is_active flag.
    References the game that it is in.
'''
class Player(models.Model):
    # bio = models.CharField(max_length=200)
    user = models.ForeignKey(User, on_delete=models.PROTECT, related_name="player") #associates each player with its corresponding user
    game = models.ForeignKey(Game, on_delete=models.PROTECT, related_name="player_game") #associates each player with a specific game instance
    wallet = models.DecimalField(max_digits=6, decimal_places = 2) #associates each player with their own wallet (amount of money they have)
    seat_number = models.IntegerField(default=0) #associates each player with their own specific seat # at the table
    picture = models.FileField(blank=True) #associates each player with their own profile picture
    content_type = models.CharField(blank=True, max_length=50) #associates each player's profile picture with a corresponding content type
    is_active = models.BooleanField(default=True) #indicates if it is a player's current turn to make an action

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
class Round(models.Model):
    game = models.ForeignKey(Game, on_delete=models.PROTECT, related_name="round_game") #associates each round with a specific game/table
    current_player = models.ForeignKey(Player, on_delete=models.PROTECT, related_name='current_player') #indicates whose turn it is during each round
    pot = models.IntegerField(default=0) #indicates the pot for each round
    highest_bet = models.IntegerField(default=0) #indicates the highest bet placed per round

'''
    This is the action model. Includes each player's action and bet amount.
    References the round that it is in.
'''
class Action(models.Model):
    round = models.ForeignKey(Round, on_delete=models.PROTECT, related_name="action_round") #associates each action taken by a player with each distinct round
    player = models.ForeignKey(Player, on_delete=models.PROTECT, related_name="action_player") #associates each action to a specific player (bet, raise, check, fold)
    action_type = models.CharField(max_length=10, choices=(('bet', 'Bet'), ('call', 'Call'), ('raise', 'Raise'), ('fold', 'Fold'))) #the four action type choices: "bet", "raise", "check", "fold"
    bet_amount = models.IntegerField(default=0) #amount of money that the player has bet

