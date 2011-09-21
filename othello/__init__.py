import copy
import sys
from os import times
from board import Board, move_string, print_moves

import logging
logging.basicConfig(level='DEBUG')

def game(white_engine, black_engine, game_time=300.0, verbose=False):
    """ Run a single game. Raises RuntimeError in the event of time expiration.
    Raises LookupError in the case of a bad move. The tournament engine must
    handle these exceptions. """
    # TODO: Figure out a method of introspection to figure out which player
    # raised an exception

    # TODO: Make this a generator or coroutine to support multithreading.
    # Iteration stops at final board, makes for simple GUI on top of this.

    #initialize variables
    board = Board()
    time = { -1 : game_time, 1 : game_time }
    engine = { -1 : black_engine, 1 : white_engine }

    # do rounds
    for move_num in range(60):
        moves = []
        for color in [-1, 1]:
            start_time = times()[0] #user time elapsed
            move = get_move(board, engine[color], color, move_num)
            end_time = times()[0]
            time[color] -= (end_time - start_time) 

            logging.debug("Player %(color)d has %(time)f seconds remaining" %\
                            {'color' : color, 'time' : time[color]})
            if time[color] < 0:
                raise RuntimeError(
                    "Player %(color)d literally has a RuntimeError" 
                        % {'color' : color })

            # make a move, otherwise pass
            if move is not None:
                board.execute_move(move, color)
                moves.append(move)
                logging.info(
                    "Round %(move_num)2d: Player %(color)d flipped %(move)s"
                        % { 'color' : color,   
                            'move' : move_string(move), 
                            'move_num' : move_num })

                if verbose:
                    board.display()

        #test for game over
        if not moves:
            logging.info("No legal moves remaining. The game is over.")
            break

    return board

def winner(board):
    """ Determines the winner of a given board. """
    # TODO: Migrate to board.py
    black_count = board.count(-1)
    white_count = board.count(1)
    if black_count > white_count:
        logging.info("Player -1 (Black) has won the game!")
        return -1
    elif white_count > black_count:
        logging.info("Player 1 (White) has won the game!")
        return 1
    else:
        logging.info("The game is a draw.")
        return None
            

def get_move(board, engine, color, move_num, **kwargs):
    """ Gets the move for the given engine and color. Has a few short circuits
    for verification of move."""
    legal_moves = board.get_legal_moves(color)

    if not legal_moves:
        return None
    elif len(legal_moves) == 1:
        return legal_moves[0]
    else:
        move = engine.get_move(copy.deepcopy(board), color, move_num, kwargs)

        if move not in legal_moves:
            raise LookupError(
                "Move not in legal moves list for player %d" % color )

        return move
    

if __name__ == '__main__':
    # TODO: Migrate to the argparse module
    if len(sys.argv) != 3:
        print "Usage: " + sys.argv[0] + " white_engine black_engine"
        print "\tex: " + sys.argv[0] + " random human"
        sys.exit()

   
    # TODO: surely, there is a better way?
    white_engine = sys.argv[1]
    black_engine = sys.argv[2]
    engines_w = __import__('engines.' + white_engine)
    engines_b = __import__('engines.' + black_engine)
    engine_w = engines_w.__dict__[white_engine].__dict__['engine']()
    engine_b = engines_b.__dict__[black_engine].__dict__['engine']()
    print black_engine, "vs.", white_engine

    board = game(engine_w, engine_b, verbose=True)
    winner = winner(board)
    if winner == -1:
        print "WINNER:", black_engine, "(black)"
    elif winner == 1:
        print "WINNER:", white_engine, "(white)"
    else:
        print "DRAW!"
