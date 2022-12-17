# A clone of https://github.com/IcePear-Jzx/Othello-AI

import pygame
from Othello.chessboard import Chessboard
from Othello.images import Images
from Othello.utils import draw
from config import *


def main():

    # set parameters
    SCREEN_WIDTH = WIDTH
    SCREEN_HEIGHT = HEIGHT
    BLACK = PLAYER_TWO

    # init
    pygame.init()
    screen = pygame.display.set_mode([SCREEN_WIDTH, SCREEN_HEIGHT])
    pygame.display.set_caption(TITLE)

    # load images
    images = Images()

    # init chessboard
    chessboard = Chessboard()

    while True:
        draw(screen, images, chessboard)
        pygame.display.update()


if __name__ == "__main__":
    main()
