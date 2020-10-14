import socket
import math

from network_utils import run_network, send_paddle, send_ball
from colorama import Fore
import pygame as pg


class Game:

    def __init__(self, screen_rect: pg.Rect, fps: int, ip: str = '', port: int = 5050, host: bool = True):
        self.fps = fps
        self.host = host
        if host:
            self.ip = socket.gethostbyname(socket.gethostname() + ".local")
        else:
            self.ip = ip
        self.port = port
        self.screen_rect = screen_rect
        self.paddle = Paddle(screen_rect[3], (screen_rect.width / 20, screen_rect.height / 5),
                             [0, (screen_rect.height / 2)], fps)
        self.other_paddle = Paddle(screen_rect[3], (screen_rect.width / 20, screen_rect.height / 5),
                                   [screen_rect.width - screen_rect.width / 20, (screen_rect.height / 2)], fps)
        self.ball = Ball(screen_rect[2], (screen_rect.center[0], screen_rect.center[1]), fps)
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
        if host:
            self.socket.bind((self.ip, port))
            self.connection = None
        else:
            self.connection = self.socket
        self.disconnect = False

    def update(self):
        self.ball.move()
        self.upper_bound()
        if self.bounds():
            send_ball(self, self.connection)
        if self.bounce():
            vel = self.ball.velocity + 0.1
            if vel > self.paddle.width:
                vel = self.paddle.width - self.paddle.width / 10
            self.ball.velocity = vel
            send_ball(self, self.connection)
        send_paddle(self, self.connection)

    def bounds(self):
        if self.ball.pos_x < 0:
            print(f"{Fore.MAGENTA}You lost that round!")
            return True
        elif self.ball.pos_x > self.screen_rect[2]:
            print(f"{Fore.MAGENTA}You won that round!")
            self.ball.pos_x = self.screen_rect[2] / 2
            self.ball.pos_y = self.screen_rect[3] / 2
            self.ball.dir_x = 1
            self.ball.dir_y = 0
            self.ball.velocity = 0.2
            return True
        return False

    def upper_bound(self):
        if self.ball.pos_y < 0 or self.ball.pos_y > self.screen_rect[3]:
            self.ball.dir_y = -self.ball.dir_y

    def bounce(self):
        collide = self.paddle.rect.collidepoint(self.ball.pos_x, self.ball.pos_y)
        if collide:
            angle = (self.ball.pos_y - self.paddle.rect.centery) / (self.paddle.height / 2) * 60
            print(angle)
            self.ball.dir_x = math.cos(math.radians(angle))
            self.ball.dir_y = math.sin(math.radians(angle))
            return True
        return False

    def start(self):
        if self.host:
            print(f"{Fore.CYAN}Server is starting...")
            self.socket.listen()
            print(f"{Fore.CYAN}Server is listening on {Fore.YELLOW + self.ip}...")
            print(self.paddle.rect.center)
            conn, addr = self.socket.accept()
            print(f"{Fore.YELLOW}{addr} {Fore.CYAN}connected\n{Fore.YELLOW}")
            self.connection = conn
        else:
            print(f"{Fore.CYAN}Connecting to server at {Fore.YELLOW}{self.ip}")
            try:
                self.socket.connect((self.ip, self.port))
            except TimeoutError:
                print(f"{Fore.CYAN}Connection timed out. (Server might not be running)")
                quit()

        self.ball.dir_x = -1
        run_network(self, self.connection)

    def stop(self):
        pass


class Paddle:

    def __init__(self, field_height: int, size: tuple, position: list, fps: int):
        self.field_height = field_height
        self.width, self.height = size
        self.position = position
        self.fps = fps
        self.rect = pg.Rect(self.position[0], self.position[1] - int(self.height / 2), self.width, self.height)

    def move(self, direction):
        if self.rect.centery + (self.height / 2) > self.field_height and direction == 'down':
            return
        if self.rect.centery - (self.height / 2) < 0 and direction == 'up':
            return
        if direction == "up":
            self.rect.centery -= self.height / self.fps * 2
        elif direction == "down":
            self.rect.centery += self.height / self.fps * 2


class Ball:

    def __init__(self, field_width: int, position: tuple, fps: int, direction: tuple = (0, 0), velocity: float = 0.2):
        self.field_width = field_width
        self.pos_x, self.pos_y = position
        self.fps = fps
        self.dir_x, self.dir_y = direction
        self.velocity = velocity

    def move(self):
        self.pos_x += self.dir_x * self.velocity * self.field_width / self.fps
        self.pos_y += self.dir_y * self.velocity * self.field_width / self.fps
