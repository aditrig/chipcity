from __future__ import annotations
import random
from .card import Card

from chipcity.models import *

class Deck:
    _FULL_DECK = []
    def __init__(self):
        self.shuffle()

    def shuffle(self):
        # and then shuffle
        self.cards = Deck.GetFullDeck()
        random.shuffle(self.cards)

    def draw(self, n=1):
        if n == 1:
            return self.cards.pop(0)

        cards = []
        for i in range(n):
            cards.append(self.draw())
        return cards

    def __str__(self):
        return Card.print_pretty_cards(self.cards)

    @staticmethod
    def GetFullDeck():
        if Deck._FULL_DECK:
            return list(Deck._FULL_DECK)

        # create the standard 52 card deck
        for rank in Card.STR_RANKS:
            for suit,val in Card.CHAR_SUIT_TO_INT_SUIT.items():
                Deck._FULL_DECK.append(Card.new(rank + suit))

        return list(Deck._FULL_DECK)

class Game_Action:
    def __init__(self):
        self.round = Game.curr_round

    def start_new_game(self, game_id):
        game = Game.objects.get(id=game_id)
        
        # Reset pot and highest bet for the round
        # round_instance = Round.objects.get_or_create(game=game, defaults={'pot': 0, 'highest_bet': 0})
        
        # Deal cards to players 
        deck = Deck()
        deck.shuffle()
        # for player in game.players.all():
        #     hand = Hand.objects.get_or_create(game=game, player=player)
        #     hand.card_left, hand.card_right = deck.draw(2)  # Assuming draw returns two card objects
        #     hand.save()

        game.flop1 = deck.draw()
        game.flop2 = deck.draw()
        game.flop3 = deck.draw()
        game.turn = deck.draw()
        game.river = deck.draw()
        
        # # Set the first player as the current player
        # round_instance.current_player = game.players.first()
        # round_instance.save()

    def round_action(self, game_id, player_id, action_type):
        self.player_action(game_id, player_id, action_type, bet_amount=0)
        self.round += 1

    def player_action(self, game_id, player_id, action_type, bet_amount=0):
        game = Game.objects.get(id=game_id)
        player = Player.objects.get(id=player_id)
        current_round = game.round_game.last()
        
        action = Action(round=current_round, player=player, action_type=action_type, bet_amount=bet_amount)
        action.save()
        
        #possible moves
        if action_type == 'bet' or action_type == 'raise':
            current_round.pot += bet_amount
            if bet_amount > current_round.highest_bet:
                current_round.highest_bet = bet_amount
        elif action_type == 'call':
            current_round.pot += current_round.highest_bet
            action.bet_amount = current_round.highest_bet  
            action.save()
        elif action_type == 'fold':
            player.hand.is_active = False
            player.hand.save()
        
        current_round.save()


# evaluator = Evaluator()

# deck = Deck()
# board = deck.draw(5)
# player1_hand = deck.draw(2)
# player2_hand = deck.draw(2)
# player3_hand = deck.draw(2)
# player4_hand = deck.draw(2)
# player5_hand = deck.draw(2)
# player6_hand = deck.draw(2)

# Card.print_pretty_cards(board)
# Card.print_pretty_cards(player1_hand)
# Card.print_pretty_cards(player2_hand)
# Card.print_pretty_cards(player3_hand)
# Card.print_pretty_cards(player4_hand)
# Card.print_pretty_cards(player5_hand)
# Card.print_pretty_cards(player6_hand)

# p1_score = evaluator.evaluate(board, player1_hand)
# p2_score = evaluator.evaluate(board, player2_hand)
# p3_score = evaluator.evaluate(board, player3_hand)
# p4_score = evaluator.evaluate(board, player4_hand)
# p5_score = evaluator.evaluate(board, player5_hand)
# p6_score = evaluator.evaluate(board, player6_hand)
# p1_class = evaluator.get_rank_class(p1_score)
# p2_class = evaluator.get_rank_class(p2_score)
# p3_class = evaluator.get_rank_class(p3_score)
# p4_class = evaluator.get_rank_class(p4_score)
# p5_class = evaluator.get_rank_class(p5_score)
# p6_class = evaluator.get_rank_class(p6_score)

# hands = [player1_hand, player2_hand, player3_hand, player4_hand, player5_hand, player6_hand]
# evaluator.hand_summary(board, hands)