# A clone of https://github.com/IcePear-Jzx/Othello-AI
import pygame


class Images:

    def __init__(self):
        self.width = 50

        self.header = pygame.image.load('static/header.png')
        self.help = pygame.image.load('static/help-button.png')
        self.undo = pygame.image.load('static/undo.png')
        self.background = pygame.image.load('static/background.png')

        self.black = pygame.image.load('static/black.png')
        self.white = pygame.image.load('static/white.png')
        self.white_available = pygame.image.load('static/white-available.png')
        self.black_available = pygame.image.load('static/black-available.png')
        self.black_transparent = pygame.image.load('static/black-transparent.png')
        self.white_transparent = pygame.image.load('static/white-transparent.png')
        self.available_transparent = pygame.image.load('static/white-available-transparent.png')
        self.white_available_transparent = pygame.image.load('static/white-available-transparent.png')
        self.black_available_transparent = pygame.image.load('static/black-available-transparent.png')
        self.tile = pygame.image.load('static/tile.png')

