from random import Random
from .card import Card

from chipcity.models import *

class Card:
    def __init__(self, suit, rank):
        self.suit = suit
        self.rank = rank

    def show(self):
        print("{} of {}".format(self.rank, self.suit))

class Deck:
    def __init__(self, seed: int = None) -> None:
        self._random = Random(seed)
        self.shuffle()

    def shuffle(self) -> None:
        # and then shuffle
        self.cards = Deck.GetFullDeck()
        self._random.shuffle(self.cards)

    def draw(self, n: int = 1) -> list[int]:
        cards = []
        for _ in range(n):
            cards.append(self.cards.pop())
        return cards

    def __str__(self) -> str:
        return Card.ints_to_pretty_str(self.cards)

    @staticmethod
    def GetFullDeck() -> list[int]:
        if Deck._FULL_DECK:
            return list(Deck._FULL_DECK)

        # create the standard 52 card deck
        for rank in Card.STR_RANKS:
            for suit in Card.STR_SUITS:
                Deck._FULL_DECK.append(Card.new(rank + suit))

        return list(Deck._FULL_DECK)

class Round_Action:
    def start_new_round(game_id):
        game = Game.objects.get(id=game_id)
        
        # Reset pot and highest bet for the round
        round_instance, created = Round.objects.get_or_create(game=game, defaults={'pot': 0, 'highest_bet': 0})
        
        # Deal cards to players 
        deck = Deck()
        deck.shuffle()
        for player in game.players.all():
            hand, created = Hand.objects.get_or_create(game=game, player=player)
            hand.card_left, hand.card_right = deck.draw(2)  # Assuming draw returns two card objects
            hand.save()
        
        # Set the first player as the current player
        round_instance.current_player = game.players.first()
        round_instance.save()

    def player_action(game_id, player_id, action_type, bet_amount=0):
        game = Game.objects.get(id=game_id)
        player = Player.objects.get(id=player_id)
        current_round = game.round_game.last()  # Assuming this retrieves the current round
        
        action = Action(round=current_round, player=player, action_type=action_type, bet_amount=bet_amount)
        action.save()
        
        # Example action handling
        if action_type == 'bet' or action_type == 'raise':
            current_round.pot += bet_amount
            if bet_amount > current_round.highest_bet:
                current_round.highest_bet = bet_amount
        elif action_type == 'call':
            # Match the highest bet
            current_round.pot += current_round.highest_bet
            action.bet_amount = current_round.highest_bet  # Update the action's bet_amount to match the highest bet
            action.save()
        elif action_type == 'fold':
            player.hand.is_active = False  # Assuming each player has one hand related to them
            player.hand.save()
        
        current_round.save()


card = Card("Hearts", 6)
card.show()

