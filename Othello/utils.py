import pygame
from config import *

def draw(screen, images, chessboard):

    btns = {}
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
    help_btn = Button(x=920, y=610)
    w = images.help.get_width()
    h = images.help.get_height()
    help_btn.draw_img(screen, images.help, w, h)
    btns['help'] = help_btn

    # draw undo button
    undo_btn = Button(x=850, y=610)
    w = images.undo.get_width()
    h = images.undo.get_height()
    undo_btn.draw_img(screen, images.undo, w, h)
    btns['undo'] = undo_btn

    # draw chesses
    for i in range(row):
        for j in range(col):
            color = images.tile
            chess = chessboard.chesses[i][j]
            if chess == WHITE:
                color = images.white
            elif chess == BLACK:
                color = images.black
            elif chess == -1 and chessboard.offense ==  WHITE:
                color = images.white_available
            elif chess == -1 and chessboard.offense == BLACK:
                color = images.black_available

            x = (margin + j * width + width // 2 - images.width // 2)
            y = (margin + i * width + width // 2 - images.width // 2)

            screen.blit(color, (x,y))

    # draw count
    pos = margin * 2 + chessboard.width * col
    if chessboard.offense == WHITE:
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

    if help_btn.hover():
        a = (WIDTH - images.help_info.get_width()) // 2
        b = images.header.get_height()
        # draw help info
        help_info = Button(x=a, y=b)
        w = images.help_info.get_width()
        h = images.help_info.get_height()
        help_info.draw_img(screen, images.help_info, w, h)

    return btns



class Button:
    def __init__(
        self,
        x=0, y=0,
        width=10,
        height=10,
        text='Button',
        roundness=0
    ):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.text = text
        self.roundness = roundness
        self.hidden = False

    def draw_img(self, screen, img, x, y):
        self.img = img
        self.width = x
        self.height = y
        screen.blit(img, (self.x, self.y))

    def click(self, mouse_pos):
        mouse_x, mouse_y = mouse_pos
        return self.x <= mouse_x <= self.x + self.width and \
            self.y <= mouse_y <= self.y + self.height

    def hover(self):
        """
        This function will return True if the cursor
        is on top of the Button object.
        False, otherwise.
        """
        rect = self.img.get_rect()
        rect.x = self.x
        rect.y = self.y
        print(rect.x, rect.y)
        return rect.collidepoint(pygame.mouse.get_pos())
