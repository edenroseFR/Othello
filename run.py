import pygame
from Othello.chessboard import Chessboard, ChessboardTreeNode, ChessboardTree
from Othello.images import Images
from Othello.utils import draw
from config import *


def main():

    # set parameters
    SCREEN_WIDTH = WIDTH
    SCREEN_HEIGHT = HEIGHT

    # init
    pygame.init()
    screen = pygame.display.set_mode([SCREEN_WIDTH, SCREEN_HEIGHT])
    pygame.display.set_caption(TITLE)

    player = BLACK

    # load images
    images = Images()

    # init chessboard
    chessboard = Chessboard()
    node = ChessboardTreeNode(chessboard)
    chessboardTree = ChessboardTree(node)
    chessboardTree.expandTree()

    draw(screen, images, chessboard)
    pygame.display.update()


    while True:
        # catch events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.MOUSEBUTTONUP:
                set_i = set_j = -1
                if chessboard.offense == player:
                    px, py = pygame.mouse.get_pos()
                    set_i = (py - chessboard.margin) // chessboard.width
                    set_j = (px - chessboard.margin) // chessboard.width
                else:
                    set_i, set_j = chessboardTree.findBestChess(player)
                if (set_i, set_j) in chessboard.available:
                    chessboardTree.root = chessboardTree.root.kids[(
                        set_i, set_j)]
                    chessboard = chessboardTree.root.chessboard
                    # update screen
                    draw(screen, images, chessboard)
                    pygame.display.update()
                    # expand only 1 layer
                    chessboardTree.expandTree()
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_b:
                    if chessboardTree.root.parent:
                        chessboardTree.root = chessboardTree.root.parent
                        chessboard = chessboardTree.root.chessboard
                        # update screen
                        draw(screen, images, chessboard)
                        pygame.display.update()


if __name__ == "__main__":
    main()
