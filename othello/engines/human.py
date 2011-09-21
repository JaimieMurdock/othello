"""
Eric P. Nichols
Feb 8, 2008

This is a human move engine; it simply reads and validates user input
to get the move to make.
"""


from board import print_moves
from engines import Engine

class HumanEngine(Engine):
    """ Human move engine that uses input to get the move to make. """
    def get_move(self, board, color, move_num=None,
                 time_remaining=None, time_opponent=None):
        """ Provides an interactive console for the human player to make moves.
        Uses parse_input to actually process the data. """
        # generate the legal moves.
        legal_moves = board.get_legal_moves(color)
   
        # request the move
        input = raw_input("Enter your move: ")
        move = HumanEngine.parse_input(legal_moves, input)
        while move is None:
            print "That move is not valid. The legal moves are:"
            print_moves(legal_moves)
            input = raw_input("\nEnter your move: ")
            move = HumanEngine.parse_input(legal_moves, input)

        return move
        
    @staticmethod
    def parse_input(legal_moves, input):
        """ Verifies that the move is in the list of moves. Returns either a
        valid move or None if the move is invalid. """
        # verify length
        if len(input) == 2:
            xc = input[0]
            yc = input[1]

            # validate range
            if xc>='a' and xc <='h' and yc>='1' and yc <='8':
                x = ord(xc)-ord('a') # convert letter to number from 0 to 7
                y = int(yc)-1        # convert numeral to int from 0 to 7
    
                # create the move
                move = (x,y)
    
                # validate legality
                if move in legal_moves:
                    return move 
                else:
                    return None

engine = HumanEngine
