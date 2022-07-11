"""This file runs the auction functions of an auction game."""
import numpy as np


class Auction:
    """The Auction is a game, involving a set of Bidders on one side, and a set of
    Users on the other. Each round represents an event in which a User navigates
    to a website with a space for an ad. When this happens, the Bidders will place
    bids, and the winner gets to show their ad to the User. The User may click on
    the ad, or not click, and the winning Bidder gets to observe the User's
    behavior. This is a second price sealed-bid Auction.
    """

    def __init__(self, users, bidders):
        self.users = users
        self.bidders = bidders
        self.bidders_list = list(range(len(bidders)))
        self.balances = {key: 0 for key in set(self.bidders_list)}
        self.user_id = None
        self.bids_list = None
        self.winner = None

    def __repr__(self):
        return f"Bidder balances are {self.balances}"

    def execute_round(self):
        """Each round is executed by choosing a user, creating bidder instances,
        receiving the bids from the bidders and selecting a winner. The winner
        pays the secon-highest bid, and receives $1 if the user clicks on the ad.
        Only the winner is notified if the user clicks.
        """
        if len(self.bidders) > 1:
            #  Choose user, see if user clicked on ad
            self.user_id = np.random.randint(0, len(self.users))

            #  Create bidders, pick winning bid
            self.bids_list = [self.bidders[i].bid(self.user_id) for i in range(len(self.bidders))]
            self.winner = self.bids_list.index(max(self.bids_list))

            #  Second-highest bid is cost, + $1 if user clicked
            self.bids_list.pop(self.winner)
            self.balances[self.winner] = round(self.balances[self.winner] - max(self.bids_list), 2)
            if self.users[self.user_id].show_ad() is True:
                self.balances[self.winner] += 1

            #  Notify only the winner
            for i, j in enumerate(self.bidders):
                if i == self.winner:
                    j.notify(True, max(self.bids_list), self.users[self.user_id].show_ad())
                else:
                    j.notify(False, max(self.bids_list), None)


class User:
    """There are num_users Users, numbered from 0 to num_users - 1. The number
    corresponding to a user will be called its user_id. Each user has a secret
    probability of clicking, whenever it is shown an ad. The probability is the
    same, no matter which Bidder gets to show the ad, and the probability never
    changes. The events of clicking on each ad are mutually independent. When a
    user is created, the secret probability is drawn from a uniform distribution
    from 0 to 1.
    """

    def __init__(self):
        # Each user has a secret probability of clicking on an ad.
        self.__probability = np.random.uniform()

    def __repr__(self):
        return "User with a probability of " + str(self.__probability)

    def show_ad(self):
        """Returns True if user clicks on ad based on secret probability.
        """
        return np.random.choice([True, False], p=[self.__probability, 1 - self.__probability])
