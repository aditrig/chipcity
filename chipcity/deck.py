from random import shuffle

class Card:
    def __init__(self, suit, rank):
        self.suit = suit
        self.rank = rank

    def show(self):
        print("{} of {}".format(self.rank, self.suit))

class Deck:
    def __init__(self):
        pass


card = Card("Hearts", 6)
card.show()

