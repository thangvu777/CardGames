# Description: Mini Blackjack game for 1-6 players
import random

class Card(object):
    RANKS = (1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13)

    SUITS = ("C", "D", "H", "S")

    def __init__(self, rank=12, suit="S"):
        # Q of spades
        if rank in Card.RANKS:
            self.rank = rank
        else:
            self.rank = 12

        if suit in Card.SUITS:
            self.suit = suit
        else:
            self.suit = "S"

    def __str__(self):
        if (self.rank == 1):
            rank = 'A'
        elif (self.rank == 13):
            rank = 'K'
        elif (self.rank == 12):
            rank = 'Q'
        elif (self.rank == 11):
            rank = 'J'
        else:
            rank = str(self.rank)
        # return string
        return rank + self.suit

    def __eq__(self, other):
        return (self.rank == other.rank)

    def __ne__(self, other):
        return (self.rank != other.rank)

    def __lt__(self, other):
        return (self.rank < other.rank)

    def __le__(self, other):
        return (self.rank <= other.rank)

    def __gt__(self, other):
        return (self.rank > other.rank)

    def __ge__(self, other):
        return (self.rank >= other.rank)


class Deck(object):
    def __init__(self):
        self.deck = []
        for suit in Card.SUITS:
            # rank before suit
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


class Player(object):
    # cards = (card1,...,cardn)
    def __init__(self, cards):
        self.cards = cards
        # introduce bust parameter
        self.bust = False

    # hitting function
    def hit(self, card):
        self.cards.append(card)

    # return card string + " "
    def get_cards(self):
        hand_str = ""
        for card in self.cards:
            hand_str = hand_str + str(card) + " "

        return hand_str

    def get_points(self):
        # count = points
        count = 0
        for card in self.cards:
            if card.rank >= 10:
                count += 10
            elif card.rank == 1:
                count += 11
            else:
                count = count + card.rank

        # deduct 10 if Ace is there and and needed as 1
        for card in self.cards:
            if count <= 21:
                break
            elif card.rank == 1:
                count = count - 10

        return count

    def busted_hand(self):
        self.bust = True


class Dealer(Player):
    def __init__(self, cards):
        super(Dealer, self).__init__(cards)

    # show dealer's first card
    def get_first_card(self):
        card_str = str(self.cards[0])
        return card_str


class Blackjack(object):
    def __init__(self, num_players):
        # make a deck
        self.deck = Deck()
        self.deck.shuffle()
        # list of all players' cards
        self.players = []
        # intent : append hand[] to players[]
        cards_num = 2

        for i in range(num_players):
            # dealing 2 cards to each hand
            hand = []
            for j in range(cards_num):
                hand.append(self.deck.deal())
            self.players.append(Player(hand))

        # dealer's hand
        hand_dealer = []
        for j in range(cards_num):
            hand_dealer.append(self.deck.deal())
        self.dealer = (Dealer(hand_dealer))

    # play
    def play(self):
        print()
        # print player's cards and points
        for i in range(len(self.players)):
            print('Player ' + str(i + 1) + ": " + self.players[i].get_cards() + "- " + str(
                self.players[i].get_points()) + " points")

        # print out the dealer's cards and points
        print('Dealer: ' + self.dealer.get_first_card())
        print()

        # hitting
        for i in range(len(self.players)):
            player = self.players[i]
            # user input for hit (y/n)
            hit_user = "y"
            while hit_user != "n" and player.get_points() < 21:
                hit_user = input("Player " + str(i + 1) + ", do you want to hit? [y / n]: ")
                if hit_user == "y":
                    player.hit(self.deck.deal())
                    print('Player ' + str(i + 1) + ": " + self.players[i].get_cards() + "- " + str(
                        self.players[i].get_points()) + " points")

            # get points, if points > 21, hand is busted. self.bust == True.
            if player.get_points() > 21:
                player.busted_hand()
            print()

        # hit dealer if points < 17
        while self.dealer.get_points() <= 16:
            self.dealer.hit(self.deck.deal())

        print('Dealer: ' + self.dealer.get_cards() + "- " + str(self.dealer.get_points()) + " points")

        # get points, if points > 21, hand is busted. self.bust == True.
        if self.dealer.get_points() > 21:
            self.dealer.busted_hand()

        print()

        # make a list for players who have not busted
        not_busted = []
        for player in self.players:
            if not player.bust:
                not_busted.append(player)

        # check who wins/loses/ties
        if self.dealer.bust:
            for i, player in enumerate(self.players):
                if player in not_busted:
                    print('Player', str(i + 1), 'wins')
                else:
                    print('Player', str(i + 1), 'loses')

        elif not self.dealer.bust:
            for i, player in enumerate(self.players):
                if player in not_busted:
                    if player.get_points() > self.dealer.get_points():
                        print('Player', str(i + 1), 'wins')
                    elif player.get_points() < self.dealer.get_points():
                        print('Player', str(i + 1), 'loses')
                    else:
                        print('Player', str(i + 1), 'ties')
                else:
                    # players bust
                    print('Player', str(i + 1), 'loses')

        print()
        print()

    # blackjack = 21 points with 2 cards
    def has_blackjack(self):
        return self.get_points() == 21 and len(self.cards) == 2


def main():
    # prompt user to enter the number of players
    num_players = int(input('Enter number of players: '))

    while num_players <= 0 or num_players >= 7:
        num_players = int(input('Enter number of players: '))

    # create blackjack object with num_players as the parameter
    bj_game = Blackjack(num_players)
    bj_game.play()


main()