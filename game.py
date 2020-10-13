import pygame as pg
import gui


class Game:

    def __init__(self, screen_rect, fps, ip):
        self.fps = fps
        self.ip = ip
        self.screen_rect = screen_rect
        self.paddle = Paddle()
        self.other_paddle = Paddle()

    def bounce(self, ):
        pass

    def move(self, direction):
        if direction == "up":
            pass
        elif direction == "down":
            pass


class Paddle:

    def __init__(self, size, position):
        self.size = size
        self.position = position


class Ball:

    def __init__(self, position, velocity):
        self.position = position
        self.velocity = velocity
