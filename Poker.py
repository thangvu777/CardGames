# Author: Thang Vu

#  Description: This is NOT a real poker game. Rather a poker hand simulation.
#  This game is based on the given # of players (2-6)/ The bot will deal out 5 cards each player/
#  Then each player will receive points based on how what their hand is (full house, flush, straight, three of a kind, pair, etc.)/
#  The player with the highest points will be the winner/

#  Things that could be done to improve this game:
#  1. Adjusting the way cards are dealt. (1 card at a time to each player as opposed to 5 cards at a time to one player)
#  2. Incorporate the flopping of cards and well as dealing out 2 hole cards to each player
#  3. Incoporate checking, betting, and folding
#  4. Introduce a currency system

import random
class Card(object):
	RANKS = (2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14)
	# clubs, diamonds, hearts, spades
	SUITS = ('C', 'D', 'H', 'S')

	def __init__(self, rank = 12, suit = 'S'):
		if (rank in Card.RANKS):
			self.rank = rank
		else:
			self.rank = 12

		if (suit in Card.SUITS):
			self.suit = suit
		else:
			self.suit = 'S'

	def __str__(self):
		if (self.rank == 14):
			rank = 'A'
		elif (self.rank == 13):
			rank = 'K'
		elif (self.rank == 12):
			rank = 'Q'
		elif (self.rank == 11):
			rank = 'J'
		else:
			rank = str(self.rank)
		return rank + self.suit

	def __eq__(self, other):
		return (self.rank == other.rank)

	def __ne__(self, other):
		return (self.rank != other.rank)

	def __lt__(self, other):
		return (self.rank < other.rank)

	def __gt__(self, other):
		return (self.rank > other.rank)

	def __ge__(self, other):
		return (self.rank >= other.rank)

class Deck(object):
	def __init__(self):
		self.deck = []
		for suit in Card.SUITS:
			for rank in Card.RANKS:
				card = Card(rank, suit)
				self.deck.append(card)
	def shuffle(self):
		random.shuffle(self.deck)

	def deal(self):
		if (len(self.deck) == 0):
			return None
		else:
			return self.deck.pop(0)

class Poker(object):
    def __init__(self, num_players):
        self.deck = Deck()
        self.deck.shuffle()
        self.players = []
        numcards_in_hand = 5

        for i in range(num_players):
            hand = []
            for j in range(numcards_in_hand):
                hand.append(self.deck.deal())
            self.players.append(hand)

    def play(self):
        # sort the hands of each player and print
        for i in range(len(self.players)):
            sortedHand = sorted(self.players[i], reverse=True)
            self.players[i] = sortedHand
            hand = ''
            for card in sortedHand:
                hand = hand + str(card) + ' '
            print('Player ' + str(i + 1) + ": " + hand)

        # determine the each type of hand and print
        points_hand = []  # create list to store points for each hand

        print()
        i = 0
        # determine winner and print
        for hand in self.players:
            i += 1
            c1, c2, c3, c4, c5 = hand[0].rank, hand[1].rank, hand[2].rank, hand[3].rank, hand[4].rank

            print('Player ' + str(i) + ': ', end="")
            if self.is_royal(hand):
                print('Royal Flush')
                h = 10
            elif self.is_straight_flush(hand):
                print("Straight Flush")
                h = 9
            elif self.is_four_kind(hand):
                print("Four of a Kind")
                h = 8
                if hand[0].rank != hand[1].rank:
                    c1 = hand[4].rank
                    c5 = hand[0].rank

            elif self.is_full_house(hand):
                print("Full House")
                h = 7

                if hand[1].rank != hand[2].rank:
                    c1 = hand[2].rank
                    c2 = hand[3].rank
                    c3 = hand[4].rank
                    c4 = hand[0].rank
                    c5 = hand[0].rank

            elif self.is_flush(hand):
                print("Flush")
                h = 6
            elif self.is_straight(hand):
                print("Straight")
                h = 5
            elif self.is_three_kind(hand):
                print("Three of a Kind")
                h = 4

                if hand[1].rank == hand[2].rank == hand[3].rank:
                    c1 = hand[1].rank
                    c2 = hand[2].rank
                    c3 = hand[3].rank
                    c4 = hand[0].rank
                    c5 = hand[4].rank
                elif hand[2].rank == hand[3].rank == hand[4].rank:
                    c1 = hand[2].rank
                    c2 = hand[3].rank
                    c3 = hand[4].rank
                    c4 = hand[0].rank
                    c5 = hand[1].rank
            elif self.is_two_pair(hand):
                print("Two Pair")
                h = 3

                if hand[1].rank == hand[2].rank and hand[3].rank == hand[4].rank:
                    c1 = hand[1].rank
                    c2 = hand[2].rank
                    c3 = hand[3].rank
                    c4 = hand[4].rank
                    c5 = hand[0].rank
                elif hand[0].rank == hand[1].rank and hand[3].rank == hand[4].rank:
                    c3 = hand[3].rank
                    c4 = hand[4].rank
                    c5 = hand[2].rank
            elif self.is_one_pair(hand):
                print("One Pair")
                h = 2

                if hand[1].rank == hand[2].rank:
                    c1 = hand[1].rank
                    c2 = hand[2].rank
                    c3 = hand[0].rank
                elif hand[2].rank == hand[3].rank:
                    c1 = hand[2].rank
                    c2 = hand[3].rank
                    c3 = hand[0].rank
                    c4 = hand[1].rank
                elif hand[3].rank == hand[4].rank:
                    c1 = hand[3].rank
                    c2 = hand[4].rank
                    c3 = hand[0].rank
                    c4 = hand[1].rank
                # High card
            else:
                print("High Card")
                h = 1

            total_points = h * 13 ** 5 + c1 * 13 ** 4 + c2 * 13 ** 3 + c3 * 13 ** 2 + c4 * 13 + c5
            points_hand.append(total_points)

        print()
        max_points = 0
        index = []
        for i in range(len(points_hand)):
            if points_hand[i] > max_points:
                max_points = points_hand[i]
                index = [i]
            elif points_hand[i] == max_points:
                index.append(i)

        for i in index:
            print("Player " + str(i + 1) + " wins.")

    # determine if a hand is a royal flush
    def is_royal(self, hand):
        same_suit = True
        for i in range(len(hand) - 1):
            same_suit = same_suit and (hand[i].suit == hand[i + 1].suit)

        if not same_suit:
            return False

        rank_order = True
        for i in range(len(hand)):
            rank_order = rank_order and (hand[i].rank == 14 - i)

        return (same_suit and rank_order)

    def is_straight_flush(self, hand):
        return self.is_straight(hand) and self.is_flush(hand)

    def is_four_kind(self, hand):
        # ordered/sorted, so check first four then last four
        ''' Only optimized for hand of 5 cards, not more/less
        front = hand.rank[0] == hand.rank[1] == hand.rank[2] == hand.rank[3]
        back = hand.rank[1] == hand.rank[1] == hand.rank[2] == hand.rank[4]
        return front or back
        '''
        for i in range(len(hand) - 3):
            if (hand[i].rank == hand[i + 1].rank == hand[i + 2].rank == hand[i + 3].rank):
                return True
        return False

    def is_full_house(self, hand):
        front = hand[0].rank == hand[1].rank == hand[2].rank and hand[3].rank == hand[4].rank
        back = hand[0].rank == hand[1].rank and hand[2].rank == hand[3].rank == hand[4].rank
        return front or back

    def is_flush(self, hand):
        same_suit = True
        for i in range(len(hand) - 1):
            same_suit = same_suit and (hand[i].suit == hand[i + 1].suit)
        return same_suit

    def is_straight(self, hand):
        rank_order = True
        for i in range(len(hand) - 1):
            rank_order = rank_order and (hand[i].rank == hand[i + 1].rank + 1)
        return rank_order

    def is_three_kind(self, hand):
        for i in range(len(hand) - 2):
            if (hand[i].rank == hand[i + 1].rank == hand[i + 2].rank):
                return True
        return False

    def is_two_pair(self, hand):
        single_at_front = hand[1].rank == hand[2].rank and hand[3].rank == hand[4].rank and hand[2].rank != hand[3].rank
        single_in_middle = hand[0].rank == hand[1].rank and hand[3].rank == hand[4].rank
        single_at_end = hand[0].rank == hand[1].rank and hand[2].rank == hand[3].rank and hand[1].rank != hand[2].rank
        return single_at_front or single_in_middle or single_at_end

    def is_one_pair(self, hand):
        for i in range(len(hand) - 1):
            if (hand[i].rank == hand[i + 1].rank):
                return True
        return False

    def is_high_card(self, hand):
        return True

from Poker import Poker
if __name__ == '__main__':

	num_players = int(input("Enter number of players: "))
	while num_players < 2 or num_players > 6:
		num_players = int(input("Enter number of players: "))
	# create the Poker object
	game = Poker(num_players)
	# play the game (poker)
	game.play()
