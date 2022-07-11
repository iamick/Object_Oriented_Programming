"""This file runs the bidder functions of an auction game."""
import numpy as np


class Bidder:
    """There is a set of Bidders. Each Bidder begins with a balance of 0 dollars.
    The objective is to finish the game with as high a balance as possible.
    At some points during the game, the Bidder's balance may become negative,
    and there is no penalty when this occurs.
    """

    def __init__(self, num_users, num_rounds):
        self.num_users = num_users
        self.num_rounds = num_rounds
        self.users_clicked = {}
        self.user_id = []
        self.auction_winner = None
        self.price = None
        self.clicked = None


    def __repr__(self):
        return str(self.users_clicked)

    def bid(self, user_id):
        """ Returns a non-negative number in dollars as the bid."""
        #  Determine and save the current user id
        self.user_id.append(user_id)

        #  Use users_clicked to decide how much to bid
        self.num_rounds -= 1
        if self.user_id not in list(self.users_clicked):
            return np.random.random()
        elif 0 < self.users_clicked[self.user_id] < 3:
            return round(np.random.randint(1, 2) + np.random.random(), 2)
        elif 3 <= self.users_clicked[self.user_id] < 10:
            return round(np.random.randint(2, 10) + np.random.random(), 2)
        else:
            return round(np.random.randint(10, 100) + np.random.random(), 2)

    def notify(self, auction_winner, price, clicked=None):
        """Used to send information about what happened in a round back to the
        Bidder. Here, auction_winner is a boolean to represent whether the
        given Bidder won the auction (True) or not (False). price is the
        amount of the second bid, which the winner pays. If the given Bidder
        won the auction, clicked will contain a boolean value to represent
        whether the user clicked on the ad. If the given Bidder did not win
        the auction, clicked will always contain None.
        """
        self.auction_winner = auction_winner
        self.price = price
        self.clicked = clicked
        if self.auction_winner is True and self.clicked is True:
            if self.user_id[-1] not in self.users_clicked:
                self.users_clicked[self.user_id[-1]] = 1
            else:
                self.users_clicked[self.user_id[-1]] += 1
        elif self.auction_winner is True and self.clicked is False:
            if self.user_id[-1] not in self.users_clicked:
                self.users_clicked[self.user_id[-1]] = 0
            else:
                pass
        else:
            pass
        return self.users_clicked
