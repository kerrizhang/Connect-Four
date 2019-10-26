''' Project #2: Send Me On My Way
Name: Kerri Zhang
SID: 21529066
Date: 10/26/2018
'''

from collections import namedtuple
import socket
from connectfour_common import PlayerMove
import connectfour

ServerConnection = namedtuple(
    'ServerConnection',
    ['socket', 'input_stream', 'output_stream'])

class CFSProtocolError(Exception):
    pass

def make_init_action_server(connection: ServerConnection) -> bool:
    '''Print out WELCOME username after proper server connection'''
    while True:
        user_input = input("Enter valid username. One word without any spaces: \n")
        user_length = len(user_input.split())
        if user_length == 1:
            break
        else:
            print("Invalid username.")
    first_string = "I32CFSP_HELLO " + user_input
    _write_line(connection, first_string)
    server_reply = _read_line(connection)
    print(server_reply)
    if not ('WELCOME ' in server_reply):
        raise CFSProtocolError()
    second_string = "AI_GAME"
    _write_line(connection, second_string)
    print("Server Communication Established")
    return True

def connect_server() -> ServerConnection:
    '''Connect the server with the server information and port number'''
    while True:
        try:
            ip_address_and_port = _ask_for_server_info()
            ip_address, port_num = ip_address_and_port
            connection = _connect(ip_address, port_num)
            return connection
        except socket.error as exception:
            print("Server Connection Failed. Check server connection and try again.", \
                  "Error type:", type(exception))
            continue

def send_action_to_server(connection: ServerConnection, action: str, column_number: int) -> None:
    '''Send action Drop/Pop to Server'''
    read_line = _read_line_check_invalid_and_winner(connection)
    if read_line == 'READY':
        command_string = action + " "
        if action == 'D':
            command_string = 'DROP '
        elif action == 'P':
            command_string = 'POP '
        line = command_string + str(column_number)
        _write_line(connection, line)
    else:
        print("Server is not ready.")
        raise CFSProtocolError()

def read_server_action(connection: ServerConnection) -> PlayerMove:
    '''Read the server reply after client's demand'''
    read_line = _read_line_check_invalid_and_winner(connection)
    if read_line == 'OKAY':
        read_next_line = _read_line_check_invalid_and_winner(connection).split()
        action = read_next_line[0]
        column_number = int(read_next_line[1])
        return PlayerMove(action = action, column_number = column_number)
    else:
        print("Server is not ready")
        raise CFSProtocolError()

def close(connection: ServerConnection) -> None:
    '''Close all connections after game finished'''
    connection.input_stream.close()
    connection.output_stream.close()
    connection.socket.close()

def error_close(connection: ServerConnection) -> None:
    '''socket.error cannot handle output_stream close'''
    connection.input_stream.close()
    connection.socket.close()

def _ask_for_server_info() -> tuple:
    '''Ask for server information and port number in one loop'''
    while True:
        ip_address = input("Enter server information \n")
        try:
            port = int(input("Enter port number \n"))
            if (port < 0 or port > 65535):
                print("Invalid port number. Port must be between 0 and 65535.")
                continue
            else:
                break
        except ValueError:
            print("Port number does not exist. Try again.")
            continue
    return (ip_address, port)

def _connect(host: str, port: int) -> ServerConnection:
    '''Establish a connection from client input'''
    server_socket = socket.socket()
    server_socket.connect((host, port))
    input_stream_object = server_socket.makefile('r')
    output_stream_object = server_socket.makefile('w')

    return ServerConnection(
        socket = server_socket,
        input_stream = input_stream_object,
        output_stream = output_stream_object)

def _write_line(connection: ServerConnection, line: str) -> None:
    '''Send line to Server '''
    connection.output_stream.write(line + '\r\n')
    connection.output_stream.flush()
    print("MESSAGE SENT TO SERVER: ", line)

def _read_line(connection: ServerConnection) -> str:
    '''Read line from Server'''
    return connection.input_stream.readline()[:-1]

def _read_line_check_invalid_and_winner(connection: ServerConnection) -> str:
    '''After server line received, check if invalid or winner and raise
    and exception'''
    line_received = _read_line(connection)
    print("SERVER: ", line_received)
    if line_received == 'INVALID':
        raise connectfour.InvalidMoveError()
    elif (line_received == 'WINNER_RED') or (line_received == 'WINNER_YELLOW'):
        raise connectfour.GameOverError()
    return line_received
