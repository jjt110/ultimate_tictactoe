"""
Board class that controls Tic Tac Toe board.
"""

from enum import Enum
import random
import math

# Enums representing game result.
class GameResultEnum(Enum):
    STILL_RUNNING = 1
    O_WIN = 2
    X_WIN = 3
    TIE = 4

class ShownEnum(Enum):
    BLANK = 1
    O = 2
    X = 3
    T = 4

def _is_valid_new_tup(new_tup, tup, num_xs, num_ys):
    if new_tup == tup:
        return False
    if new_tup[0] < 0 or new_tup[0] >= num_xs:
        return False
    if new_tup[1] < 0 or new_tup[1] >= num_ys:
        return False
    return True


# Ultimate Tic Tac Toe Board. Represents the entire board, including each of 
# its individual Tic Tac Toe games.
class UltimateTicTacToeBoard:
    # Class representing Tic Tac Toe Board
    class TicTacToeBoard:
        def __init__(self, x_cord, y_cord):
            self.x_cord = x_cord    #1...3
            self.y_cord = y_cord    #1...3
            self.num_xs = 3
            self.num_ys = 3
            self.squares = {}
            self.square_edges = {}
            self.square_shown_state = ShownEnum.BLANK
            self.board_full = False
        
        # Sets up the game with given input. Sets up the squares
        def set_up(self):
            print('setting up')
            for x in range(3):
                self.squares[x] = {}
                for y in range(3):
                    self.squares[x][y] = self.Square(x, y)
            
            # Set up edges for each square.
            for x in range(3):
                for y in range(3):
                    tup = (x, y)
                    edges = []
                    for x_change in (-1, 0, 1):
                        for y_change in (-1, 0, 1):
                            new_tup = (x + x_change, y + y_change)
                            if _is_valid_new_tup(new_tup, tup,
                                                 self.num_xs, self.num_ys):
                                edges.append(new_tup)
                    self.square_edges[tup] = edges
        
        # Print the board for the user.
        def print_board(self, debug=False):
            x_break = "    "
            x_label = "    "
            for x in range(self.num_xs):
                x_break += "---"
                x_label += (" %s " % str(x))
            print(x_label)
            print(x_break)
            
            for y in reversed(range(self.num_ys)):
                y_row_to_print = ("|")
                for x in range(self.num_xs):
                    square = self.squares[x][y]
                y_row_to_print += ("|")
                print(y_row_to_print)
    
            print(x_break)
            print(x_label)
            print("")
            
        # Identifies if Board has won
        def check_win(self, x_cord, y_cord):
            orig_square = self.squares[x_cord][y_cord]
            
            tup=(x_cord,y_cord)
            traverse_list = []
            for edge_tup in self.square_edges[(x_cord, y_cord)]:
                traverse_list.append(edge_tup)
            traversed_set = set()
            while traverse_list:
                # For a given square, put it to traversed_list
                (traverse_x_cord, traverse_y_cord) = traverse_list.pop()
                if (traverse_x_cord, traverse_y_cord) in traversed_set:
                    continue
                traversed_set.add((traverse_x_cord, traverse_y_cord))
                square = self.squares[traverse_x_cord][traverse_y_cord]
    
                if square.square_shown_state == orig_square.square_shown_state:
                    direction_1 = (2*traverse_x_cord-x_cord,2*traverse_y_cord-y_cord)
                    direction_2 = (2*x_cord-traverse_x_cord,2*y_cord-traverse_y_cord)
                    if _is_valid_new_tup(direction_1,tup,self.num_xs,self.num_ys):
                        next_square = self.squares[2*traverse_x_cord-x_cord][2*traverse_y_cord-y_cord]
                        if next_square.square_shown_state == orig_square.square_shown_state:
                            self.square_shown_state = orig_square.square_shown_state
                    elif _is_valid_new_tup(direction_2,tup,self.num_xs,self.num_ys):
                        next_square = self.squares[2*x_cord-traverse_x_cord][2*y_cord-traverse_y_cord]
                        if next_square.square_shown_state == orig_square.square_shown_state:
                            self.square_shown_state = orig_square.square_shown_state
            full = True
            for x in range(self.num_xs):
                for y in range(self.num_ys):
                    if self.squares[x][y].square_shown_state == ShownEnum.BLANK:
                        full = False
            self.board_full = full
            
        # Class representing each square in tic tac toe.
        class Square:
            def __init__(self, x_cord, y_cord):
                self.x_cord = x_cord
                self.y_cord = y_cord
                self.square_shown_state = ShownEnum.BLANK
    
            def get_print_str(self):
                if self.square_shown_state == ShownEnum.BLANK:
                    return "   "
                elif self.square_shown_state == ShownEnum.O:
                    return '\033[1;31;m O \033[0;38;m'
                elif self.square_shown_state == ShownEnum.X:
                    return '\033[1;34;m X \033[0;38;m'
                else:
                    return " %s "

    # Set up class variables.
    def __init__(self):
        self.game_result = GameResultEnum.STILL_RUNNING
        self.num_xs = 3
        self.num_ys = 3
        self.squares = {}
        self.square_edges = {}
        self.board_full = False

    # Sets up the game with given input. Sets up the games along with all its
    # adjacent edges.
    def set_up(self):
        self.print_line_break()
        print("Setting up Ultimate Tic Tac Toe Board") 
        for x in range(3):
            self.squares[x] = {}
            for y in range(3):
                self.squares[x][y] = self.TicTacToeBoard(x, y)
                (self.squares[x][y]).set_up()

        # Set up edges for each board.
        for x in range(3):
            for y in range(3):
                tup = (x, y)
                edges = []
                for x_change in (-1, 0, 1):
                    for y_change in (-1, 0, 1):
                        new_tup = (x + x_change, y + y_change)
                        if _is_valid_new_tup(new_tup, tup,
                                             self.num_xs, self.num_ys):
                            edges.append(new_tup)
                self.square_edges[tup] = edges
    


    # Prints line break so user can see between their inputs better.
    def print_line_break(self):
        print("\n+++++++++++++++++++++++++++++++++++++++++++++++++++++\n")
    
    # Define coordinates
    def coord(self, x_cord, y_cord):
        game_x_cord = math.trunc((x_cord)/3)
        game_y_cord = math.trunc((y_cord)/3)
        
        square_x_cord = x_cord % 3        
        square_y_cord = y_cord % 3
        return (game_x_cord, game_y_cord, square_x_cord, square_y_cord)

    # Print the board for the user.
    def print_board(self, debug=False):
        self.print_line_break()

        if self.game_result == GameResultEnum.O_WIN:
            print("!!!!!!!!!!!!!!")
            print("!!! O WINS !!!")
            print("!!!!!!!!!!!!!!\n")
        elif self.game_result == GameResultEnum.X_WIN:
            print("!!!!!!!!!!!!!!")
            print("!!! X WINS !!!")
            print("!!!!!!!!!!!!!!\n")
        
        s_label = "        "
        g_label = "        "
        x_break = "        "
        x_label = "        "
        counter = 0
        for x in range(self.num_xs*self.num_xs):
            x_break += "---"
            x_label += (" %s " % str(x))
            s_label += (" %s " % str(x % 3))
            g_label += (" %s " % str(math.trunc(x/3)))
            if counter == self.num_xs-1:
                counter = 0
                x_label += " "
                s_label += " "
                g_label += " "
            else:
                counter += 1
                
        for x in range(self.num_xs):
            x_break += "--"
        x_break += '--'
        print(s_label)
        print(g_label)
        print(x_label)
        print(x_break)
        
        
        y_flag = False
        for y in reversed(range(self.num_ys*self.num_ys)):
            g = math.trunc(y/3)
            s = y % 3
            y_row_to_print = (" %s %s %s |" % (s,g,y))
            counter = 0
            board_counter = 0
            board_row_to_print = "        "
            for x in range(self.num_xs*self.num_xs):
                (game_x,game_y,square_x,square_y) = self.coord(x,y)
                board = self.squares[game_x][game_y]
                state = board.square_shown_state
                square = board.squares[square_x][square_y]   
                y_row_to_print += square.get_print_str()
                if board.square_shown_state == ShownEnum.O:
                    y_row_to_print += '\033[1;31;m|\033[0;38;m'
                elif board.square_shown_state == ShownEnum.X:
                    y_row_to_print += '\033[1;34;m|\033[0;38;m'
                elif board.square_shown_state == ShownEnum.T:
                    y_row_to_print += '\033[1;34;m|\033[0;38;m'
                else:
                    y_row_to_print += 
                if board_counter % 3 != self.num_xs-1:
                    if board.square_shown_state == ShownEnum.O:
                        y_row_to_print += '\033[1;31;m|\033[0;38;m'
                        board_row_to_print += '\033[1;31;m--- \033[0;38;m'
                    elif board.square_shown_state == ShownEnum.X:
                        y_row_to_print += '\033[1;34;m|\033[0;38;m'
                        board_row_to_print += '\033[1;34;m--- \033[0;38;m'
                    else:
                        y_row_to_print += '|'
                        board_row_to_print += '--- '
                board_counter += 1        
                board_row_to_print += '  '
                if counter == self.num_xs-1:
                    counter = 0
                    y_row_to_print += "|"
                else:
                    counter += 1
            y_row_to_print += (" %s %s %s") % (y,g,s)
            if g != math.trunc((y+1)/3) and y_flag:
                print(x_break)
            y_flag = True
            print(y_row_to_print)
            print(board_row_to_print)


        print(x_break)
        print(x_label)
        print(g_label)
        print(s_label)
        print("")
    
    # Calculates if square is valid.
    def is_valid_square(self, square):
        if square.square_shown_state != ShownEnum.BLANK:
            return False
        else:
            return True           

    # Checks if the user move is valid.
    # Two possible errors: 1) Wrong tictactoe board or 2) Square already taken
    def is_valid_move(self, x_cord, y_cord, first_move, prev_x_cord, prev_y_cord):
        (game_x_cord, game_y_cord, square_x_cord, square_y_cord) = self.coord(x_cord, y_cord)
        print(game_x_cord)
        print(game_y_cord)
        game = self.squares[game_x_cord][game_y_cord]
        square = game.squares[square_x_cord][square_y_cord]
        
        prev_square_x_cord = prev_x_cord % 3
        prev_square_y_cord = prev_y_cord % 3
        prev_game = self.squares[prev_square_x_cord][prev_square_y_cord]
        
        if self.is_valid_square(square):
            if not first_move:
                if prev_square_x_cord != game_x_cord or prev_square_y_cord != game_y_cord:
                    # If board selected to be played is full (TIE), any other board is ok
                    if prev_game.board_full:
                        return (True, "Success")
                    else:
                        return (False, "Board[%s][%s] is wrong" % (game_x_cord, game_y_cord))
                        # Add clause for right board number
                else:
                    return (True, "Success")
            else:
                return (True, "Success")
        else:
            return (False, "Square[%s][%s] is already marked" % (square_x_cord,square_y_cord))
            
    # Identifies if Board has won
    def check_win(self, x_cord, y_cord):
        orig_square = self.squares[x_cord][y_cord]
        
        tup=(x_cord,y_cord)
        traverse_list = []
        for edge_tup in self.square_edges[(x_cord, y_cord)]:
            traverse_list.append(edge_tup)
        traversed_set = set()
        while traverse_list:
            # For a given square, put it to traversed_list
            (traverse_x_cord, traverse_y_cord) = traverse_list.pop()
            if (traverse_x_cord, traverse_y_cord) in traversed_set:
                continue
            traversed_set.add((traverse_x_cord, traverse_y_cord))
            square = self.squares[traverse_x_cord][traverse_y_cord]

            if square.square_shown_state == orig_square.square_shown_state:
                direction_1 = (2*traverse_x_cord-x_cord,2*traverse_y_cord-y_cord)
                direction_2 = (2*x_cord-traverse_x_cord,2*y_cord-traverse_y_cord)
                if _is_valid_new_tup(direction_1,tup,self.num_xs,self.num_ys):
                    next_square = self.squares[2*traverse_x_cord-x_cord][2*traverse_y_cord-y_cord]
                    if next_square.square_shown_state == orig_square.square_shown_state:
                        self.square_shown_state = orig_square.square_shown_state
                elif _is_valid_new_tup(direction_2,tup,self.num_xs,self.num_ys):
                    next_square = self.squares[2*x_cord-traverse_x_cord][2*y_cord-traverse_y_cord]
                    if next_square.square_shown_state == orig_square.square_shown_state:
                        self.square_shown_state = orig_square.square_shown_state
        full = True
        for x in range(self.num_xs):
            for y in range(self.num_ys):
                if self.squares[x][y].square_shown_state == ShownEnum.BLANK:
                    full = False
        self.board_full = full
        if full:
            self.game_result = GameResultEnum.TIE

    # Plays the given user's input.
    def play_move(self, x_cord, y_cord, player):
        # player = 0 --> 'O'
        # player = 1 --> 'X'
        (game_x_cord, game_y_cord, square_x_cord, square_y_cord) = self.coord(x_cord, y_cord)
        game = self.squares[game_x_cord][game_y_cord]
        square = game.squares[square_x_cord][square_y_cord]
        if player == 0:
            square.square_shown_state = ShownEnum.O
        elif player == 1:
            square.square_shown_state = ShownEnum.X
        game.check_win(square_x_cord,square_y_cord)
        self.check_win(game_x_cord,game_y_cord)
        self.print_board()