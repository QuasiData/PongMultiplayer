import sys
import pygame as pg


SCREEN_SIZE = (810, 810)
FPS = 10
BACKGROUND = pg.Color("white")


class App:
    def __init__(self):
        self.screen = pg.display.get_surface()
        self.screen_rect = self.screen.get_rect()
        self.clock = pg.time.Clock()
        self.done = False

    def update(self):
        """
        All updates to all actors occur here.
        Exceptions include things that are direct results of events which
        may occasionally occur in the event loop.

        For example, updates based on held keys should be found here, but
        updates to single KEYDOWN events would be found in the event loop.
        """

        for event in pg.event.get():
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_UP:
                    # Move paddle up
                    pass
                elif event.key == pg.K_DOWN:
                    # Move paddle down
                    pass

    def render(self):
        """
        All calls to drawing functions here.
        No game logic.
        """
        self.screen.fill(BACKGROUND)
        #self.gui.draw(self.screen_rect)
        pg.display.update()

    def event_loop(self):
        """
        Event handling here.  Only things that are explicit results of the
        given events should be found here.  Do not confuse the event and update
        phases.
        """
        key = 0
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.done = True



    def main_loop(self):
        """
        Main loop for your whole app.  This doesn't need to be touched until
        you start writing framerate independant games.
        """
        while not self.done:
            self.event_loop()
            self.update()
            self.render()
            self.clock.tick(FPS)


def main():
    """
    Prepare pygame and the display and create an App instance.
    Call the app instance's main_loop function to begin the App.
    """
    pg.init()
    pg.display.set_mode(SCREEN_SIZE)
    App().main_loop()
    pg.quit()
    sys.exit()
    

if __name__ == "__main__":
    main()