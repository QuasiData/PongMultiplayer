import sys
import pygame as pg
from game import Game


SCREEN_SIZE = (810, 810)
FPS = 60
BACKGROUND = pg.Color("black")


class App:
    def __init__(self, host):
        self.screen = pg.display.get_surface()
        self.screen_rect = self.screen.get_rect()
        self.clock = pg.time.Clock()
        if host:
            self.game = Game(self.screen_rect, FPS)
        else:
            self.game = Game(self.screen_rect, FPS, ip="192.168.1.13", host=False)  # TODO: Implement argparse for this
        self.game.start()
        self.prev_paddle_rect = 0
        self.prev_other_paddle_rect = 0
        self.prev_ball_pos = 0
        self.first_loop = True
        self.done = False

    def draw(self):
        pg.draw.rect(self.screen, (255, 255, 255), self.game.paddle.rect)
        pg.draw.rect(self.screen, (255, 255, 255), self.game.other_paddle.rect)
        pg.draw.circle(self.screen, (255, 255, 255), (int(self.game.ball.pos_x), int(self.game.ball.pos_y)), 20)
        self.prev_paddle_rect = self.game.paddle.rect.copy()
        self.prev_other_paddle_rect = self.game.other_paddle.rect.copy()
        self.prev_ball_pos = (int(self.game.ball.pos_x), int(self.game.ball.pos_y))

    def update(self):
        """
        All updates to all actors occur here.
        Exceptions include things that are direct results of events which
        may occasionally occur in the event loop.

        For example, updates based on held keys should be found here, but
        updates to single KEYDOWN events would be found in the event loop.
        """

        keys = pg.key.get_pressed()
        if keys[pg.K_s]:
            self.game.paddle.move("down")
        elif keys[pg.K_w]:
            self.game.paddle.move("up")

        self.game.update()

    def render(self):
        """
        All calls to drawing functions here.
        No game logic.
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
        Event handling here.  Only things that are explicit results of the
        given events should be found here.  Do not confuse the event and update
        phases.
        """
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.done = True

    def main_loop(self):
        """
        Main loop for your whole app.  This doesn't need to be touched until
        you start writing framerate independent games.
        """
        while not self.done:
            self.event_loop()
            self.update()
            self.render()
            self.clock.tick(FPS)
            if self.first_loop:
                self.first_loop = False


def main(host=False):
    """
    Prepare pygame and the display and create an App instance.
    Call the app instance's main_loop function to begin the App.
    """
    pg.init()
    pg.display.set_mode(SCREEN_SIZE)
    if host:
        pg.display.set_caption("HOST")
    else:
        pg.display.set_caption("CLIENT")
    App(host).main_loop()
    pg.quit()
    sys.exit()
    

if __name__ == "__main__":
    main()
