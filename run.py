import pygame
from Othello.chessboard import Chessboard
from Othello.chessboard import ChessboardTreeNode
from Othello.chessboard import ChessboardTree
from Othello.images import Images
from Othello.utils import draw
from config import *


def revert_to_prev_state(chessboardTree):
    chessboardTree.root = chessboardTree.root.parent
    chessboard = chessboardTree.root.chessboard
    return chessboardTree.root, chessboard


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
    chessboardTree.expand_tree()


    while True:
        btns = draw(screen, images, chessboard)
        pygame.display.update()

        mouse_pos = pygame.mouse.get_pos()
        # catch events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

            elif event.type == pygame.MOUSEBUTTONUP:
                # Check if undo button is fired up
                if btns['undo'].click(mouse_pos) and \
                    chessboardTree.root.parent:
                    chessboardTree.root, chessboard = \
                        revert_to_prev_state(chessboardTree)
                    continue
                elif chessboard.offense == player:
                    mouse_x, mouse_y = mouse_pos
                    set_i = (mouse_y - chessboard.margin) // chessboard.width
                    set_j = (mouse_x - chessboard.margin) // chessboard.width
                else:
                    print('finding best position to put disc to...')
                    set_i, set_j = chessboardTree.find_best_pos(player)
                if (set_i, set_j) in chessboard.available:
                    chessboardTree.root = chessboardTree.root.kids[(
                        set_i, set_j)]
                    chessboard = chessboardTree.root.chessboard
                    # update screen
                    draw(screen, images, chessboard)
                    pygame.display.update()
                    # expand only 1 layer
                    chessboardTree.expand_tree()

            elif event.type == pygame.KEYUP and chessboardTree.root.parent:
                chessboardTree.root, chessboard = \
                    revert_to_prev_state(chessboardTree)


if __name__ == "__main__":
    main()
