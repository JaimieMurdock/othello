'''
Author: Eric P. Nichols
Date: Feb 8, 2008.

Board class.

Board data:
  1=white, -1=black, 0=empty
  first dim is column , 2nd is row:
     pieces[1][7] is the square in column 2,
     at the opposite end of the board in row 8.


Squares are stored and manipulated as (x,y) tuples. 
x is the column, y is the row.
'''
class Board():

    # list of all 8 directions on the board, as (x,y) offsets
    __directions = [(1,1),(1,0),(1,-1),(0,-1),(-1,-1),(-1,0),(-1,1),(0,1)]

    def __init__(self):
        "Set up initial board configuration."

        # Create the empty board array.
        self.__pieces = [None]*8
        for i in range(8):
            self.__pieces[i] = [0]*8

        # Set up the initial 4 pieces.
        self.__pieces[3][4] = 1
        self.__pieces[4][3] = 1
        self.__pieces[3][3] = -1;
        self.__pieces[4][4] = -1;

    # add [][] indexer syntax to the Board
    def __getitem__(self, index):
        return self.__pieces[index]

    def display(self):
        "Display the board."
        print "   -----------------------"
        for y in range(7,-1,-1):
            print y+1, "|",    # print the row #
            for x in range(8):
                piece = self[x][y]    # get the piece to print
                if piece == -1: print "b ",
                elif piece == 1: print "W ",
                else:
                    if x==7:
                        print "-",
                    else:
                        print "- ",
            # Display the # of pieces for each color to the right of the board
            if y==4:
                print "|  W: " + str(self.count(1))
            elif y==3:
                print "|  b: " + str(self.count(-1))
            else:
                print "|"

        print "   -----------------------"

        # print the column labels as letters on the bottom of the board
        print "   ",
        for x in range(8):
            print get_col_char(x), '',        # prints 'a', 'b', etc.
        print

    def count(self, color):
        """Counts the # pieces of the given color
        (1 for white, -1 for black, 0 for empty spaces)"""
        count = 0
        for y in range(8):
            for x in range(8):
                if self[x][y]==color:
                    count += 1
        return count

    def get_squares(self, color):
        """Gets coordinates (x,y pairs) for all pieces on the board of the given color.
        (1 for white, -1 for black, 0 for empty spaces)"""

        squares=[]
        for y in range(8):
            for x in range(8):
                if self[x][y]==color:
                    squares.append( (x,y) )
        return squares

        
    def get_legal_moves(self, color):
        """Returns all the legal moves for the given color.
        (1 for white, -1 for black
        """
        moves = set()  # stores the legal moves.

        # Get all the squares with pieces of the given color.
        for square in self.get_squares(color):
            # Find all moves using these pieces as base squares.
            newmoves = self.get_moves_for_square(square)
            # Store these in the moves set.
            moves.update(newmoves)

        return list(moves)


    def get_moves_for_square(self, square):
        """Returns all the legal moves that use the given square as a base.
        That is, if the given square is (3,4) and it contains a black piece,
        and (3,5) and (3,6) contain white pieces, and (3,7) is empty, one
        of the returned moves is (3,7) because everything from there to (3,4)
        is flipped.
        """
        (x,y) = square

        # determine the color of the piece.
        color = self[x][y]

        # skip empty source squares.
        if color==0: 
            return None

        # search all possible directions.
        moves = []
        for direction in self.__directions:
            move = self._discover_move(square, direction)
            if move:
                moves.append(move)

        # return the generated move list
        return moves

    def execute_move(self, move, color):
        """Perform the given move on the board; flips pieces as necessary.
        color gives the color pf the piece to play (1=white,-1=black)
        """

        #Much like move generation, start at the new piece's square and
        #follow it on all 8 directions to look for a piece allowing flipping.

        # Add the piece to the empty square.
        flips = (flip for direction in self.__directions
                      for flip in self._get_flips(move, direction, color))

        for x, y in flips:
            self[x][y] = color

    def _discover_move(self, origin, direction):
        """ Returns the endpoint for a legal move, starting at the given origin,
        moving by the given increment."""
        x, y = origin
        color = self[x][y]
        flips = []

        for x, y in Board._increment_move(origin, direction):
            if self[x][y] == 0 and flips:
                return (x, y)
            elif self[x][y] == color:
                return None 
            elif self[x][y] == -color:
                flips.append((x, y))
    
    def _get_flips(self, origin, direction, color):
        """ Gets the list of flips for a vertex and direction to use with the
        execute_move function """
        #initialize variables
        flips = [origin]

        for x, y in Board._increment_move(origin, direction):
            if self[x][y] == -color:
                flips.append((x, y))
            elif self[x][y] == color and len(flips) > 1:
                return flips

        return []

    @staticmethod
    def _increment_move(move, direction):
        """ Generator expression for incrementing moves """
        move = map(sum, zip(move, direction))
        while all(map(lambda x: 0 <= x < 8, move)):
            yield move
            move = map(sum, zip(move, direction))



def get_col_char(col):
    """ converts 1, 2,... to 'a', 'b',... """
    return chr(ord('a')+col)

def moves_string(moves):
    """Returns the given coordinate list as a nicely formatted list of moves.
    example: turns [(2,3), (5,2)] into "c4, f3" """
    s = ""
    for i, move in enumerate(moves):
        if i == len(moves)-1:
            s += move_string(move)
        else:
            s += move_string(move) + ', '
    return s

def print_moves(moves):
    """Prints the list of coordinates."""
    print moves_string(moves)

def move_string(move):
    """Converts a numeric (x,y) coordinate like (2,3) into a piece name like "c4" """
    (x,y) = move
    return get_col_char(x)+str(y+1)

if __name__ == '__main__':
    board = Board()
    board.display()

    print "black: ",
    print_moves(board.get_legal_moves(-1))

    print "white: ",
    print_moves(board.get_legal_moves(1))

