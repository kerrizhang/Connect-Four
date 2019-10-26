''' Project #2: Send Me On My Way
Name: Kerri Zhang
SID: 21529066
Date: 10/26/2018
'''

import connectfour_socket
import connectfour_common
from connectfour import GameState
from connectfour import BOARD_COLUMNS, BOARD_ROWS, NONE, RED, YELLOW
import connectfour
from connectfour_socket import ServerConnection
from connectfour_common import PlayerMove
import socket

def play_game_with_server(connection: ServerConnection, current_game: GameState) -> None:
    '''Play game with server'''
    while True:
        try:
            connectfour_common.print_turn(current_game)
            connectfour_common.print_board(current_game)
            if current_game.turn == RED:
                action_column_number = connectfour_common.ask_input(current_game)
                current_game = connectfour_common.take_action_on_input(current_game, \
                                action_column_number.action, action_column_number.column_number)
                connectfour_socket.send_action_to_server(connection, action_column_number.action, \
                                action_column_number.column_number)
            else:
                action_column_number = connectfour_socket.read_server_action(connection)
                current_game = connectfour_common.take_action_on_input(current_game, \
                                action_column_number.action, action_column_number.column_number)
            color_winner = connectfour.winner(current_game)

            if color_winner != NONE:
                connectfour_common.declare_winner(current_game, color_winner)
                connectfour_socket.close(connection)
                break

        except (connectfour.InvalidMoveError, ValueError):
            if current_game.turn == YELLOW:
                print("Invalid Server Move. Please restart Connect Four.")
                connectfour_socket.close(connection)
                break
            else:
                print("Invalid Move. Please Try Again.")
                continue

def connectfour_against_ai_main() -> None:
    '''Main function that calls functions from connectfour and connectfour_socket'''
    connection = connectfour_socket.connect_server()
    current_game = connectfour_common.new_game()
    try:
        connectfour_socket.make_init_action_server(connection)
        play_game_with_server(connection, current_game)
    except connectfour_socket.CFSProtocolError:
        connectfour_socket.close(connection)
        print("Protocol Error. Please restart Connect Four.")
    except connectfour.GameOverError:
        print("GAME OVER. No moves left.")
        connectfour_socket.close(connection)
    except socket.error as exception:
        print("Error type:", type(exception), "Please restart Connect Four.")
        connectfour_socket.error_close(connection)


if __name__ == '__main__':
    connectfour_against_ai_main()