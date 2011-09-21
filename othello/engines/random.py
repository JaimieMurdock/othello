# fix to avoid importing self
from __future__ import absolute_import
import random 

from engines import Engine

class RandomEngine(Engine):
    """ Engine that plays completely randomly. """
    def get_move(self, board, color, move_num=None,
                 time_remaining=None, time_opponent=None):
        """ Selects a random move from the list of valid moves. """
        moves = board.get_legal_moves(color)
        return random.choice(moves)

# module variable to make it easier to call engine
engine = RandomEngine

