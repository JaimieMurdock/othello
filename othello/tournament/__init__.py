#driver.__init__.py
#
#Eric P. Nichols
#Feb 8, 2009

#Runs one othello game by pitting the given two modules against each other.
#Modules are intended to run linerally, without "thinking" on the other player's clock.

#Either module may be the human-input module, to allow playing against the computer.

# the first folder given must contain an engine with the "get_white_move" fxn.
# the 2nd folder will be used with the get_black_move fxn.

# Each folder must contain a python module called get_move.py. This module
# must provide two functions, get_white_move and get_black_move.

# The folder must also contain an __init__.py file (which may be empty, but must exist)

# Each get_*_move function must return the desired move as an (x,y) tuple,
# representing the move to make as the given color.
# If a function returns an illegal move, the game is forfeit for that player.
# Moves can be selected from the list returned by board.get_legal_moves(color),
# where "color" is 1 for white or "-1" for black.
# Othello is a complete-information game, so each get_*_move call is provided
# with 4 arguments, representing the complete state of the game as known
# to both players.

# 1. board: a copy of the current board
# 2. time_remaining: the time remaining on the clock for the player-to-move, in seconds
# 3. time_opponent: the time remaining on the clock for the opponent, in seconds
# 4. move_number: the current move number in plies (from 1 to 60)

# The driver records a move log, a list of tuples of the following form:
#    (move_num, color, move_string, time_remaining)
# where
#    color is -1 or 1, and time_remaining is number of seconds left for the player
#    at the conclusion of this move

import copy
import sys

#sys.path.append('C:\\Documents and Settings\\epnichol\\My Documents\\code\\workspace2\\Othello\\src')

for p in sys.path: print p

#import fcntl
from os import times

from driver.board import Board, move_string, print_moves

PRINT_LOG = True


# white_engine is the name of the white engine module, such as "human" or "random"
# this is the name of the folder containing the get_move.py file providing
# get_white_move
# likewise for black_engine & get_black_move
def run(white_engine, black_engine, results_file_path):

    # load the specified module from the engines package.
    #engines = __import__('engines.random.get_move')
    #engine = engines.__dict__['random'].__dict__['get_move']
    engines_w = __import__('engines.' + white_engine + '.get_move')
    engines_b = __import__('engines.' + black_engine + '.get_move')
    engine_w = engines_w.__dict__[white_engine].__dict__['get_move']
    engine_b = engines_b.__dict__[black_engine].__dict__['get_move']

    board = Board()
    game_log = []

    black_time = 5 * 60.0     # 5 minutes/game * 60 seconds/min
    #black_time = 5            # 5 seconds per gmae!!
    white_time = black_time

    # black moves first
    color_to_move = -1

    # no winner yet. 1 means white won, -1 for black won, 0 for draw.
    winner = 0

    # display the initial board.
    board.display()

    winning_reason = '-'    # normal winning condition.

    for move_num in range(60):
        # first, make sure there is a legal move. If not, swap colors.
        legal_moves = board.get_legal_moves(color_to_move)
        if len(legal_moves)==0:
            # No legal moves. Pass.
            print "Move = PASS"
            # Record in log.
            if color_to_move==-1:
                game_log.append( (move_num, color_to_move, "PASS", black_time) )
            else:
                game_log.append( (move_num, color_to_move, "PASS", white_time) )

            # Swap colors and try agian.
            color_to_move *= -1
            legal_moves = board.get_legal_moves(color_to_move)
            if len(legal_moves)==0:
                # Still no legal moves: we've reached an impasse and the game is over.
                print "No legal moves remaining. The game is over."
                break

        print "White time: " + str(white_time) + "\t",
        print "Black time: " + str(black_time)

        print "Move #" + str(move_num+1) + " --",
        if color_to_move == -1: print "black"
        else: print "white"

        # Bypass engines and force the move if there is only 1 legal move.
        if len(legal_moves)==1:
            move = legal_moves[0]
        else:
            # start the clock.
            start_time = times()[0]    ## times()[0] is the user time elapsed
            if color_to_move == -1:
                # get the move.
                move = engine_b.__dict__["get_black_move"](copy.deepcopy(board),
                                                           black_time,
                                                           white_time,
                                                           move_num)
                # stop the clock.
                end_time = times()[0]
                black_time -= (end_time - start_time)

            else:
                # get the move.
                move = engine_w.__dict__["get_white_move"](copy.deepcopy(board),
                                                           white_time,
                                                           black_time,
                                                           move_num)
                # stop the clock.
                end_time = times()[0]
                white_time -= (end_time - start_time)

            # verify the move is legal
            if not move in legal_moves:
                print "ILLEGAL MOVE!"
                if color_to_move == -1: print "Black",
                else: print "White",
                print "forfeits on move " + str(move_num+1) + " with move ",
                print move_string(move)
                print "Legal moves were: "
                print_moves(legal_moves)

                winning_reason = 'IllegalMove'
                # set the winning color
                winner = color_to_move * -1
                break

            # Check the clock -- did someone go overtime?
            if white_time < 0:
                print "White ran out of time on move " + str(move_num+1)
                winner = -1
                winning_reason = 'time'
                break
            elif black_time < 0:
                print "Black ran out of time on move " + str(move_num+1)
                winner = 1
                winning_reason = 'time'
                break

        #print the move.
        move_str = move_string(move)
        print "Move = " + move_str

        # Add to the log.
        if color_to_move==-1:
            game_log.append( (move_num, color_to_move, move_str, black_time) )
        else:
            game_log.append( (move_num, color_to_move, move_str, white_time) )

        # make the move.
        board.execute_move(move, color_to_move)

        # display the resulting board.
        board.display()

        # swap the color to move
        color_to_move *= -1


    # check for winner (unless we already know due to forfeit.)
    if winner == 0:
        (winner, num_white, num_black) = board.get_winner()

        print "\nFinal Score\n-----------\nBlack: " + str(num_black) + "\tWhite: " + str(num_white)

    print "\nAnd the winner is:",
    if winner==-1: print "Black"
    elif winner==1: print "White"
    else: print "...DRAW!"

    # print the log
    if PRINT_LOG:
        print ("\nLog:\n(move_num, color, move_string, time_remaining)")
        for entry in game_log:
            print entry

    result_str = "white=" + white_engine + ",black=" + black_engine
    if winner==-1: result_str += ",winner=" + black_engine
    elif winner==1: result_str += ",winner=" + white_engine
    else: result_str += ",draw"
    result_str += ",reason=" + winning_reason

    print result_str

    # lock the results file.
    results_file = open(results_file_path, 'a')
    #fxntl.flock(results_file.fileno(), fcntl.LOCK_EX)
    # output results.
    results_file.write(result_str + "\n")
    # unlock results file.
    # TODO

    results_file.close()

if __name__ == '__main__':
    print "---------------------"
    print "Othello Driver"
    print "Eric P. Nichols, 2008"
    print "---------------------"
    # check syntax of command line
    if len(sys.argv) != 4:
        print "Usage: " + sys.argv[0] + " white_engine black_engine result_file"
        print "\tex: " + sys.argv[0] + " random human results.log"
        sys.exit()

    # check that result_file can be written to.
    results = sys.argv[3]
    #if not os.exists(results):
    #    print "Could not open file " + results + " for writing."
    #    sys.exit(1)

    run(sys.argv[1], sys.argv[2], results)