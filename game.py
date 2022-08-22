"""
Main Python function for running the tic tac toe. Helps create the game
board and interact with user through input.
"""

from enum import Enum
import board
import random

# Helps interact with the player and the board.
class GameMaster:

    def __init__(self):
        pass

    def start_game(self,debug):
        # Initialize board with the given input.
        self.ms_board = board.UltimateTicTacToeBoard()
        self.ms_board.set_up()
        first_move = True
        prev_x_cord = 0
        prev_y_cord = 0
        player = 1
        
        # While game is still running, get next move from user, then try to play
        # that move.
        # O starts
        while self.ms_board.game_result == board.GameResultEnum.STILL_RUNNING:
            next_move_flag = True
            while next_move_flag:
                if debug:
                    x_cord = random.randint(0,8)
                    y_cord = random.randint(0,8)
                    next_move_flag = False
                    #debug = False
                else:
                    (x_cord, y_cord, next_move_flag) = self.get_next_move()
            (is_valid_move, err_msg) = self.ms_board.is_valid_move(
                x_cord,y_cord,first_move,prev_x_cord,prev_y_cord)

            if not is_valid_move:
                print("\nInvalid Move at x-cord: %s - y-cord: %s" % (x_cord, y_cord))
                print(" *Error Message: %s" % err_msg)
                print(self.ms_board.print_board())
                continue
            
            self.ms_board.play_move(x_cord,y_cord,player%2)
            prev_x_cord = x_cord
            prev_y_cord = y_cord
            first_move = False
            player +=1

        # Once the game is done, show the board.
        self.ms_board.print_board(True)

    # Gets input from user for the next move. Should give x_cord, y_cord, and
    # num_flags (0 to indicate no mine).
    def get_next_move(self):
        while True:
            print("Enter x coordinate - (0...8)")
            x_cord = input("0...8: ")
            try:
                x_cord = int(x_cord)
            except:
                print("%s is not a valid int." % x_cord)
                continue
            if x_cord < 0 or x_cord > 8:
                print("%s is out of bounds." % x_cord)
            else:
                break

        while True:
            print("Enter y coordinate - (0...8, X to undo)")
            y_cord = input("0...8, X: ")
            try:
                y_cord = int(y_cord)
            except:
                if y_cord == "X":
                    return (0, 0, True)
                else:
                    print("%s is not a valid int." % y_cord)
                continue
            if y_cord < 0 or y_cord > 8:
                print("%s is out of bounds." % y_cord)
            else:
                break

        return (x_cord, y_cord, False)


game_master = GameMaster()
game_master.start_game(True)
