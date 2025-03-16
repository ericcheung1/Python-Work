import string
import random
import functools

suits = ["S", "C", "D", "H"]
longsuits = ["spades", "clubs", "diamonds", "hearts"]

ranks = ["2", "3", "4", "5", "6", "7", "8", "9", "T", "J", "Q", "K", "A"]
longranks = [
    "two",
    "three",
    "four",
    "five",
    "six",
    "seven",
    "eight",
    "nine",
    "ten",
    "jack",
    "queen",
    "king",
    "ace",
]

ranklist = "".join(ranks)

ranklookup = {}
for i in range(len(ranks)):
    ranklookup[ranks[i]] = i

suitlookup = {}
for i in range(len(suits)):
    suitlookup[suits[i]] = i


@functools.total_ordering
class Card:
    """
    Class to hold information about a single playing card.  The card's rank
    and suit are stored.

    The constructor takes two arguments, the rank and suit of the card.  The
    rank and suit must be values from the ranks and suits list.

    >>> c1 = Card('8', 'C')
    >>> c2 = Card('K', 'H')
    >>> print(c1)
    8C
    >>> print(c2)
    KH
    """

    def __init__(self, rank: str, suit: str):
        self.__rank = ranklookup[rank]
        self.__suit = suitlookup[suit]

    def __eq__(self, other: object) -> bool:
        return (
            isinstance(other, Card)
            and self.__rank == other.__rank
            and self.__suit == other.__suit
        )

    def __lt__(self, other: "Card") -> bool:
        """
        Implement ordering for card objects (along with functools.total_ordering).

        >>> c1 = Card('8', 'C')
        >>> c2 = Card('K', 'H')
        >>> c1<c2
        True
        >>> c1>c2
        False
        >>> c1==c2
        False
        """
        if self.__rank != other.__rank:
            return self.__rank < other.__rank
        else:
            return self.__suit < other.__suit

    def __str__(self) -> str:
        """
        Return a two-character string representing the card.

        >>> c1 = Card('8', 'C')
        >>> str(c1)
        '8C'
        """
        return self.shortname()

    def __repr__(self) -> str:
        """
        Return a the Python code required to construt the card.

        >>> c1 = Card('8', 'C')
        >>> print(repr(c1).split(".",1)[1])
        Card('8', 'C')
        """
        return "%s.Card(%r, %r)" % (
            self.__module__,
            ranks[self.__rank],
            suits[self.__suit],
        )

    def suit(self) -> str:
        """
        Return a character representing the card's suit.  This will be one of the
        characters from suits.

        >>> c1 = Card('8', 'C')
        >>> c1.suit()
        'C'
        """
        return suits[self.__suit]

    def rank(self) -> str:
        """
        Return a character with the card's rank.  This will be one of the
        characters from ranks.

        >>> c1 = Card('8', 'C')
        >>> c1.rank()
        '8'
        """
        return ranks[self.__rank]

    def shortname(self) -> str:
        """
        Output a short two-character description of the card.

        >>> c1 = Card('8', 'C')
        >>> c1.shortname()
        '8C'
        """
        return ranks[self.__rank] + suits[self.__suit]

    def longname(self) -> str:
        """
        Return a long English description of the card.

        >>> c1 = Card('8', 'C')
        >>> c1.longname()
        'eight of clubs'
        """
        return longranks[self.__rank] + " of " + longsuits[self.__suit]


testhand = [
    Card("9", "H"),
    Card("6", "C"),
    Card("7", "S"),
    Card("6", "D"),
    Card("A", "H"),
]


def deck() -> list[Card]:
    """
    Return an *unshuffled* deck of cards (list of card objects).

    >>> d = deck()
    >>> print(hand_display(d))
    2S 3S 4S 5S 6S 7S 8S 9S TS JS QS KS AS 2C 3C 4C 5C 6C 7C 8C 9C TC JC QC KC AC 2D 3D 4D 5D 6D 7D 8D 9D TD JD QD KD AD 2H 3H 4H 5H 6H 7H 8H 9H TH JH QH KH AH
    >>> print(len(d))
    52
    """
    d = []
    for suit in range(len(suits)):
        for rank in range(len(ranks)):
            c = Card(ranks[rank], suits[suit])
            d.append(c)

    return d


def small_deck() -> list[Card]:
    """
    Return a small *unshuffled* deck of cards (list of card objects).  This is
    smaller than a regular deck and can be used for testing.

    >>> d = small_deck()
    >>> print(hand_display(d))
    9S TS JS QS KS AS 9C TC JC QC KC AC 9D TD JD QD KD AD 9H TH JH QH KH AH
    >>> print(len(d))
    24
    """
    d = []
    for suit in range(len(suits)):
        for rank in [7, 8, 9, 10, 11, 12]:
            c = Card(ranks[rank], suits[suit])
            d.append(c)

    return d


def hand_display(hand: list[Card]) -> str:
    """
    Create a string that represents the cards in the player's hand.

    >>> hand_display(testhand)
    '9H 6C 7S 6D AH'
    >>> hand_display([])
    ''
    """

    return " ".join([c.shortname() for c in hand])


if __name__ == "__main__":
    import doctest
    doctest.testmod()

