import sys

import pygame as pg
from game import Game


SCREEN_SIZE = (810, 810)
BACKGROUND = pg.Color("black")
FPS = 60


class App:
    """
    An App object. Keeps track of data concerning the flow of the game
    and initialises a Game
    """
    def __init__(self, host: bool, port: int, ip: str):
        self.screen = pg.display.get_surface()
        self.screen_rect = self.screen.get_rect()
        self.clock = pg.time.Clock()
        if host:
            self.game = Game(screen_rect=self.screen_rect, fps=FPS, port=port, host=host)
        else:
            self.game = Game(screen_rect=self.screen_rect, fps=FPS, ip=ip, port=port, host=host)
        self.game.start()
        self.prev_paddle_rect = None
        self.prev_other_paddle_rect = None
        self.prev_ball_pos = None
        self.first_loop = True
        self.done = False

    def draw(self):
        """
        Draws the paddles and ball and copies their position
        """
        pg.draw.rect(self.screen, (255, 255, 255), self.game.paddle.rect)
        pg.draw.rect(self.screen, (255, 255, 255), self.game.other_paddle.rect)
        pg.draw.circle(self.screen, (255, 255, 255), (int(self.game.ball.pos_x), int(self.game.ball.pos_y)), 20)
        self.prev_paddle_rect = self.game.paddle.rect.copy()
        self.prev_other_paddle_rect = self.game.other_paddle.rect.copy()
        self.prev_ball_pos = (int(self.game.ball.pos_x), int(self.game.ball.pos_y))

    def update(self):
        """
        Updates all actors in game and moves paddles based on key held
        """
        keys = pg.key.get_pressed()
        if keys[pg.K_e]:
            self.game.paddle.move(1)
        elif keys[pg.K_d]:
            self.game.paddle.move(-1)
        self.game.update()

    def render(self):
        """
        Uses method draw to draw everything on the screen and update it
        """
        if self.first_loop:
            self.screen.fill(BACKGROUND)
            self.draw()
        else:
            pg.draw.rect(self.screen, (0, 0, 0), self.prev_paddle_rect)
            pg.draw.rect(self.screen, (0, 0, 0), self.prev_other_paddle_rect)
            pg.draw.circle(self.screen, (0, 0, 0), self.prev_ball_pos, 20)
            self.draw()
        pg.display.update()

    def event_loop(self):
        """
        Handles single key presses and events
        """
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.done = True

    def main_loop(self):
        """
        Main loop for the game
        """
        while not self.done:
            self.event_loop()
            self.update()
            self.render()
            self.clock.tick(FPS)
            if self.first_loop:
                self.first_loop = False
        self.game.stop()


def main(host: bool, port: int, ip: str):
    """
    Initialises pygame and screen.
    Creates an App object and calls its main_loop method

    Args:
        host(bool): True if this App should act as host
        port(int): The port of the connection
        ip(str): IP address to connect to if not host
    """
    pg.init()
    pg.display.set_mode(SCREEN_SIZE)
    if host:
        pg.display.set_caption("HOST")
    else:
        pg.display.set_caption("CLIENT")
    App(host, port, ip).main_loop()
    pg.quit()
    sys.exit()
