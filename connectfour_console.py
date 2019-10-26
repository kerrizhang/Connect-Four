''' Project #2: Send Me On My Way
Name: Kerri Zhang
SID: 21529066
Date: 10/26/2018
'''

import connectfour
import connectfour_common
from connectfour import BOARD_COLUMNS, BOARD_ROWS, NONE, RED, YELLOW
from connectfour import GameState
from connectfour_common import PlayerMove

def connectfour_console_main() -> None:
    '''Main function calls from connectfour and connectfour_common'''
    current_game = connectfour_common.new_game()
    while True:
        try:
            connectfour_common.print_turn(current_game)
            connectfour_common.print_board(current_game)
            action_column_number = connectfour_common.ask_input(current_game)
            current_game = connectfour_common.take_action_on_input(current_game,  \
                            action_column_number.action, action_column_number.column_number)
            color_winner = connectfour.winner(current_game)
        except connectfour.InvalidMoveError:
            print("Invalid Move. Please Try Again.")
            continue
        except connectfour.GameOverError:
            print("GAME OVER. No moves left.")
            break
        if color_winner != NONE:
            connectfour_common.declare_winner(current_game, color_winner)
            break

if __name__ == '__main__':
    connectfour_console_main()