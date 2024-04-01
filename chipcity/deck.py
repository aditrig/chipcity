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
    def __init__(self, round, player, action):
        self.round = round
        self.player = player
        self.action = action

    def Start_Round(self):
        for p in Game.player_game.all():
            Hand.card_left = Deck.draw()
            Hand.card_right = Deck.draw()
        
        Game.flop1 = Deck.draw()
        Game.flop2 = Deck.draw()
        Game.flop3 = Deck.draw()
        Game.total_pot = 0
    
    def Round_2():
        pass


card = Card("Hearts", 6)
card.show()

