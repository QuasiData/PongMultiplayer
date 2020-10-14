import threading

from colorama import Fore
from socket import socket


def read_payload(payload):
    # Kind of a meh function currently
    if len(payload.split(",")) > 1:
        return 'ball'


def update_game(game, conn: socket):
    """
    Receives updates about the ball and paddle
    of the other game. Runs on a separate thread.

    Args:
        game(Game): Current Game object
        conn(socket): The socket the game is connected to
    """
    connected = True
    while connected:
        try:
            header = conn.recv(32).decode("utf-8")
            if header:
                length = header.split(" ")[0]
                payload = conn.recv(int(length)).decode('utf-8')
                if read_payload(payload) == 'ball':
                    payload = payload.strip('()')
                    data = payload.split(',')
                    pos_x, pos_y, dir_x, dir_y, vel = [float(x) for x in data]
                    data = game.screen_rect[2] - pos_x, pos_y, -dir_x, dir_y, vel
                    game.ball.pos_x, game.ball.pos_y, game.ball.dir_x, game.ball.dir_y, game.ball.velocity = data
                else:
                    game.other_paddle.rect.centery = int(payload)
        except ConnectionAbortedError or ConnectionResetError as e:
            print(f"{Fore.RED}{e}")
            connected = False
    conn.close()
    game.disconnect = True


def send_paddle(game, conn: socket):
    """
    Sends the y position of the paddle
    to the other game

    Args:
        game(Game): Current Game object
        conn(socket): The socket the game is connected to
    """
    try:
        y = game.paddle.rect.centery
        payload = f"{y}".encode('utf-8')
        arg = f"{len(payload)}".encode('utf-8')
        header = arg + b" " * (32 - len(arg))
        msg = header + payload
        conn.sendall(msg)
    except ConnectionAbortedError or ConnectionResetError as e:
        print(f"{Fore.RED}{e}")
        conn.close()


def send_ball(game, conn: socket):
    """
    Sends the position, direction and velocity
    of the ball to the other game

    Args:
        game(Game): Current Game object
        conn(socket): The socket the game is connected to
    """
    try:
        pos_x, pos_y = game.ball.pos_x, game.ball.pos_y
        dir_x, dir_y = game.ball.dir_x, game.ball.dir_y
        vel = game.ball.velocity
        payload = f"{pos_x,pos_y,dir_x,dir_y,vel}".encode('utf-8')
        arg = f"{len(payload)}".encode('utf-8')
        header = arg + b" " * (32 - len(arg))
        msg = header + payload
        conn.sendall(msg)
    except ConnectionAbortedError or ConnectionResetError as e:
        print(f"{Fore.RED}{e}")
        conn.close()


def run_network(game, conn: socket):
    """
    Starts a thread of the function update_game

    Args:
        game(Game): Current Game object
        conn(socket): The socket the game is connected to
    """
    thread_update = threading.Thread(target=update_game, args=(game, conn))
    thread_update.start()
