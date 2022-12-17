from config import *

class Chessboard:

    def __init__(self):
        self.width = TILE_WIDTH
        self.row = self.col = 8
        self.margin = TILE_MARGIN
        self.chesses = self.generate_board()
        self.stable_chesses = self.generate_board()
        # black on the offensive
        self.offense = 2
        # init white chesses
        self.chesses[self.row // 2 - 1][self.col // 2 - 1] = 1
        self.chesses[self.row // 2][self.col // 2] = 1
        # init black chesses
        self.chesses[self.row // 2][self.col // 2 - 1] = 2
        self.chesses[self.row // 2 - 1][self.col // 2] = 2
        # init count
        self.count_black = self.count_white = 2
        self.count_available = 4
        self.count_stable_black = 0
        self.count_stable_white = 0
        self.count_total_stable_direct_black = 0
        self.count_total_stable_direct_white = 0
        # init available pos
        self.available = []
        self.updateAvailable()

    def generate_board(self):
        '''
        returns an array of eight arrays
        [
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0]
        ]
        '''
        return [[0 for _ in range(self.col)] for _ in range(self.row)]


    def updateAvailable(self):
        directions = [(0, 1), (0, -1), (1, 0), (-1, 0),
                      (1, 1), (-1, -1), (1, -1), (-1, 1)]
        color = self.offense
        color_reverse = 3 - color
        # clear available pos
        self.available = []
        for i in range(self.row):
            for j in range(self.col):
                if self.chesses[i][j] == -1:
                    self.chesses[i][j] = 0
        # find available pos
        for i in range(self.row):
            for j in range(self.col):
                if self.chesses[i][j] == self.offense:
                    for dx, dy in directions:
                        checking_i = i + dy
                        checking_j = j + dx
                        find_one_reverse_color = False
                        while 0 <= checking_i < self.row and 0 <= checking_j < self.col:
                            chess = self.chesses[checking_i][checking_j]
                            if chess == color_reverse:
                                checking_i += dy
                                checking_j += dx
                                find_one_reverse_color = True
                            elif chess == 0 and find_one_reverse_color:
                                self.chesses[checking_i][checking_j] = -1
                                # find available pos, add it into self.available
                                self.available.append((checking_i, checking_j))
                                break
                            else:
                                break


    # reverse chesses
    def reverse(self, set_i, set_j):
        directions = [(0, 1), (0, -1), (1, 0), (-1, 0),
                      (1, 1), (-1, -1), (1, -1), (-1, 1)]
        color_reverse = self.offense
        color = 3 - color_reverse
        for dx, dy in directions:
            checking_i = set_i + dy
            checking_j = set_j + dx
            while 0 <= checking_i < self.row and 0 <= checking_j < self.col:
                chess = self.chesses[checking_i][checking_j]
                if chess == color_reverse:
                    checking_i += dy
                    checking_j += dx
                elif chess == color:
                    reversing_i = set_i + dy
                    reversing_j = set_j + dx
                    while (reversing_i, reversing_j) != (checking_i, checking_j):
                        self.chesses[reversing_i][reversing_j] = color
                        reversing_i += dy
                        reversing_j += dx
                    break
                else:
                    break


    def updateStable(self):
        directions = [(0, 1), (1, 0), (1, 1), (1, -1)]
        find_new_stable_chess = True
        while find_new_stable_chess:
            find_new_stable_chess = False
            self.count_total_stable_direct_black = 0
            self.count_total_stable_direct_white = 0
            for i in range(self.row):
                for j in range(self.col):
                    if (self.chesses[i][j] == 1 or self.chesses[i][j] == 2) and not self.stable_chesses[i][j]:
                        count_stable_direction = 0
                        for direction in directions:
                            if self.checkDirectionStable(i, j, direction):
                                count_stable_direction += 1
                        if count_stable_direction == 4:
                            find_new_stable_chess = True
                            self.stable_chesses[i][j] = 1
                        else:
                            if self.chesses[i][j] == 1:
                                self.count_total_stable_direct_white += count_stable_direction
                            elif self.chesses[i][j] == 2:
                                self.count_total_stable_direct_black += count_stable_direction


    def checkDirectionStable(self, i, j, direction):
        directions = [direction, (-direction[0], -direction[1])]
        color = self.chesses[i][j]
        color_reverse = 3 - color
        count_tmp = 0
        for dx, dy in directions:
            find_unstable_chess = False
            checking_i = i + dy
            checking_j = j + dx
            while True:
                if not (0 <= checking_i < self.row and 0 <= checking_j < self.col):
                    if find_unstable_chess:
                        count_tmp += 1
                        break
                    else:
                        return True
                if self.chesses[checking_i][checking_j] == color:
                    if self.stable_chesses[checking_i][checking_j]:
                        return True
                    else:
                        checking_i += dy
                        checking_j += dx
                        find_unstable_chess = True
                elif self.chesses[checking_i][checking_j] == color_reverse:
                    if self.stable_chesses[checking_i][checking_j]:
                        count_tmp += 1
                        break
                    else:
                        checking_i += dy
                        checking_j += dx
                        find_unstable_chess = True
                else:
                    break
        if count_tmp == 2:
            return True
        else:
            return False


    def updateCount(self):
        self.count_black = self.count_white = 0
        self.count_available = 0
        self.count_stable_white = self.count_stable_black = 0
        for i in range(self.row):
            for j in range(self.col):
                chess = self.chesses[i][j]
                if chess == 1:
                    self.count_white += 1
                elif chess == 2:
                    self.count_black += 1
                elif chess == -1:
                    self.count_available += 1
                if self.stable_chesses[i][j] == 1:
                    if self.chesses[i][j] == 1:
                        self.count_stable_white += 1
                    elif self.chesses[i][j] == 2:
                        self.count_stable_black += 1


    def copy(self):
        chessboard_new = Chessboard()
        chessboard_new.offense = self.offense
        chessboard_new.available = [item for item in self.available]
        for i in range(self.row):
            for j in range(self.col):
                chessboard_new.chesses[i][j] = self.chesses[i][j]
                chessboard_new.stable_chesses[i][j] = self.stable_chesses[i][j]
        chessboard_new.count_black = self.count_black
        chessboard_new.count_white = self.count_white
        chessboard_new.count_available = self.count_available
        chessboard_new.count_stable_black = self.count_stable_black
        chessboard_new.count_stable_white = self.count_stable_white
        chessboard_new.count_total_stable_direct_black = self.count_total_stable_direct_black
        chessboard_new.count_total_stable_direct_white = self.count_total_stable_direct_white
        return chessboard_new
