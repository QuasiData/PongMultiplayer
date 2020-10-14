import threading

from colorama import Fore
from socket import socket


def read_payload(payload):
    if len(payload.split(",")) > 1:
        return 'ball'


def update_game(game, conn: socket):
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
    thread_update = threading.Thread(target=update_game, args=(game, conn))
    thread_update.start()

