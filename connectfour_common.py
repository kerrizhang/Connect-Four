''' Project #2: Send Me On My Way
Name: Kerri Zhang
SID: 21529066
Date: 10/26/2018
'''

import connectfour
from connectfour import BOARD_COLUMNS, BOARD_ROWS, NONE, RED, YELLOW
from connectfour import GameState
import collections

PlayerMove = collections.namedtuple('PlayerMove', ['action', 'column_number'])

def new_game() -> GameState:
    '''Start of new game'''
    print("Welcome to the game of Connect Four!")
    current_game = connectfour.new_game()
    return current_game

def print_board(game: GameState) -> None:
    '''Print the board layout'''
    for columns in range(0, BOARD_COLUMNS):
        string_to_print = " "+ str(columns+1) + " "
        print(string_to_print, end = '')
    print()
    for rows in range(0, BOARD_ROWS):
        for columns in range(0, BOARD_COLUMNS):
            if game.board[columns][rows] == 0:
                print(' . ', end = '')
            elif game.board[columns][rows] == 1:
                print(' R ', end = '')
            elif game.board[columns][rows] == 2:
                print(' Y ', end = '')
        print()

def print_turn(current_game: GameState) -> None:
    '''Print Red/Yellow turn before board layout'''
    if current_game.turn == RED:
        print("It's player Red's turn.")
    elif current_game.turn == YELLOW:
        print("It's player Yellow's turn.")

def ask_input(current_game: GameState) -> PlayerMove:
    '''Ask for input about action and column number'''
    while True:
        try:
            user_input = input("Specify 'D' for Drop or 'P' for Pop followed by a space and " \
            "column number 1-7.\n").split()
            length = len(user_input)
            if length == 2:
                action = user_input[0].upper()
                column_number = int(user_input[1])
                if 1 <= column_number <= 7 and (action == 'D' or action == 'P'):
                    break
                else:
                    print("INVALID ENTRY. Must have 'D/P' followed by a space and one digit(#1-7)")
                    continue
            else:
                print("INVALID ENTRY. Must have 'D/P' followed by a space and one digit(#1-7)")
        except ValueError:
            print("Invalid Column Number. Please Try Again.")

    return PlayerMove(action = action, column_number = column_number)

def take_action_on_input(current_game: GameState, action: str, column_number: int) -> GameState:
    '''Make sure move is valid to take action'''
    if (action == "D") or (action == 'DROP'):
        updated_game = connectfour.drop(current_game, column_number - 1)
    elif (action == 'P') or (action == 'POP'):
        updated_game = connectfour.pop(current_game, column_number - 1)
    else:
        updated_game = current_game
        print("Something went wrong. Not able to take action. Please restart Connect Four.")
        raise connectfour.InvalidMoveError
    return updated_game

def declare_winner(current_game: GameState, color_winner: int) -> None:
    '''Declare a winner to end game'''
    print_board(current_game)
    if color_winner == RED:
        print("PLAYER RED IS THE WINNER.")
    elif color_winner == YELLOW:
        print("PLAYER YELLOW IS THE WINNER.")
    print("GAME OVER. Thanks for playing!")