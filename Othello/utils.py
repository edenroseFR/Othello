import pygame
from config import *

def draw(screen, images, chessboard):

    # draw backgroud
    screen.blit(images.background, (0, 0))

    # draw grid
    width = chessboard.width
    row = chessboard.row
    col = chessboard.col
    margin = chessboard.margin

    # draw header
    screen.blit(images.header, (0,0))

    # draw help button
    screen.blit(images.help, (920, 610))

    # draw undo button
    screen.blit(images.undo, (850, 610))


    # draw chesses
    for i in range(row):
        for j in range(col):
            color = images.tile
            chess = chessboard.chesses[i][j]
            if chess == WHITE:
                color = images.white
            elif chess == BLACK:
                color = images.black
            elif chess == -1 and chessboard.offense == 1:
                color = images.white_available
            elif chess == -1 and chessboard.offense == 2:
                color = images.black_available

            x = (margin + j * width + width // 2 - images.width // 2)
            y = (margin + i * width + width // 2 - images.width // 2)

            screen.blit(color, (x,y))

    # draw count
    pos = margin * 2 + chessboard.width * col
    if chessboard.offense == 1:
        screen.blit(images.black_available_transparent, (pos, pos // 2 - images.width * 1.5))
        screen.blit(images.white_transparent, (pos, pos // 2 + images.width * 0.5))
    else:
        screen.blit(images.black_transparent, (pos, pos // 2 - images.width * 1.5))
        screen.blit(images.white_available_transparent, (pos, pos // 2 + images.width * 0.5))
    fontObj = pygame.font.Font(None, images.width)
    textSurfaceObj = fontObj.render(str(chessboard.count_black), True, (0, 0, 0))
    textRectObj = textSurfaceObj.get_rect()
    textRectObj.center = (pos + images.width * 2, pos // 2 - images.width)
    screen.blit(textSurfaceObj, textRectObj)
    textSurfaceObj = fontObj.render(str(chessboard.count_white), True, (0, 0, 0))
    textRectObj = textSurfaceObj.get_rect()
    textRectObj.center = (pos + images.width * 2, pos // 2 + images.width)
    screen.blit(textSurfaceObj, textRectObj)