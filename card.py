# -*- coding: utf-8 -*-


class Card(object):
    """
    https://github.com/worldveil/deuces
    Static class that handles cards. We represent cards as 8-bit integers, so
    there is no object instantiation - they are just ints. Most of the bits are
    used, and have a specific meaning. See below:

                    Card:

                    suit rank
                    +--------+
                    |cdhsrrrr|
                    +--------+

        1) r = rank of card (trey=0,four=1,five=2,...,ace=11,deuce=12,
                             Black-Joker=13,Colored-Joker=14)
        2) cdhs = suit of card (bit turned on based on suit of card)
    """

    # the basics
    STR_RANKS = '3-4-5-6-7-8-9-10-J-Q-K-A-2-BJ-CJ'.split('-')
    INT_RANKS = range(15)

    # converstion from string => int
    CHAR_RANK_TO_INT_RANK = dict(zip(STR_RANKS, INT_RANKS))
    CHAR_SUIT_TO_INT_SUIT = {
        's': 1,  # spades
        'h': 2,  # hearts
        'd': 4,  # diamonds
        'c': 8,  # clubs
    }
    INT_SUIT_TO_CHAR_SUIT = ' shxdxxxc'

    # for pretty printing
    PRETTY_SUITS = {
        0: '',
        1: u"\u2660".encode('utf-8'),  # spades
        2: u"\u2764".encode('utf-8'),  # hearts
        4: u"\u2666".encode('utf-8'),  # diamonds
        8: u"\u2663".encode('utf-8')   # clubs
    }

    # hearts and diamonds
    PRETTY_REDS = [2, 4]

    @staticmethod
    def new(string):
        if string in Card.STR_RANKS[-2:]:
            return Card.CHAR_RANK_TO_INT_RANK[string]

        rank_char = string[:-1]
        suit_char = string[-1]
        rank_int = Card.CHAR_RANK_TO_INT_RANK[rank_char]
        suit_int = Card.CHAR_SUIT_TO_INT_SUIT[suit_char]

        suit = suit_int << 4

        return suit | rank_int

    @staticmethod
    def int_to_str(card_int):
        rank_int = Card.get_rank_int(card_int)
        suit_int = Card.get_suit_int(card_int)
        return Card.STR_RANKS[rank_int] + Card.INT_SUIT_TO_CHAR_SUIT[suit_int]

    @staticmethod
    def rank_int_to_str(card_int):
        rank_int = Card.get_rank_int(card_int)
        return Card.STR_RANKS[rank_int]

    @staticmethod
    def cards_without_suit(card_ints):
        no_suit_cards = [Card.rank_int_to_str(ci) for ci in card_ints]
        return '-'.join(no_suit_cards)

    @staticmethod
    def get_rank_int(card_int):
        return (card_int) & 0xF

    @staticmethod
    def get_suit_int(card_int):
        return (card_int >> 4) & 0xF

    @staticmethod
    def int_to_pretty_str(card_int):
        """
        Prints a single card
        """

        color = False
        try:
            from termcolor import colored
            # for mac, linux: http://pypi.python.org/pypi/termcolor
            # can use for windows: http://pypi.python.org/pypi/colorama
            color = True
        except ImportError:
            pass

        # suit and rank
        suit_int = Card.get_suit_int(card_int)
        rank_int = Card.get_rank_int(card_int)

        # if we need to color red
        s = Card.PRETTY_SUITS[suit_int]
        if color and suit_int in Card.PRETTY_REDS:
            s = colored(s, "red")

        r = Card.STR_RANKS[rank_int]

        return " [ " + r + " " + s + " ] "

    @staticmethod
    def print_pretty_card(card_int):
        """
        Expects a single integer as input
        """
        print Card.int_to_pretty_str(card_int)

    @staticmethod
    def print_pretty_cards(card_ints):
        """
        Expects a list of cards in integer form.
        """
        output = " "
        for i in range(len(card_ints)):
            c = card_ints[i]
            if i != len(card_ints) - 1:
                output += Card.int_to_pretty_str(c) + ","
            else:
                output += Card.int_to_pretty_str(c) + " "

        print output
