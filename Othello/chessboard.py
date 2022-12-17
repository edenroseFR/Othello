from config import *

class Chessboard:

    def __init__(self):
        self.width = TILE_WIDTH
        self.row = self.col = 8
        self.margin = TILE_MARGIN
        self.chesses = self.generate_board()
        self.stable_chesses = self.generate_board()
        # black on the offensive
        self.offense = BLACK
        # init count
        self.count_black = 2
        self.count_white = 2
        self.count_available = 4
        self.count_stable_black = 0
        self.count_stable_white = 0
        self.count_total_stable_direct_black = 0
        self.count_total_stable_direct_white = 0
        # init available pos
        self.available = []
        self.set_initial_position()
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

    def set_initial_position(self):
        '''
        Modifies the board so that the initial state becomes

        [
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, w, b, 0, 0, 0],
            [0, 0, 0, b, w, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0]
        ]
        '''
        # init white chesses
        self.chesses[self.row // 2 - 1][self.col // 2 - 1] = 1
        self.chesses[self.row // 2][self.col // 2] = 1
        # init black chesses
        self.chesses[self.row // 2][self.col // 2 - 1] = 2
        self.chesses[self.row // 2 - 1][self.col // 2] = 2

    def updateAvailable(self):
        # TODO: Understand the tuples
        directions = [
            (0, 1), (0, -1), (1, 0), (-1, 0),
            (1, 1), (-1, -1), (1, -1), (-1, 1)
        ]

        color = self.offense
        color_reverse = 3 - color
        # clear available pos
        self.available = []
        for i in range(self.row):
            for j in range(self.col):
                if self.chesses[i][j] == -1:
                    self.chesses[i][j] = 0
        # find available pos that the offensive can move to
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
        directions = [
            (0, 1), (0, -1), (1, 0), (-1, 0),
            (1, 1), (-1, -1), (1, -1), (-1, 1)
        ]

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


class ChessboardTreeNode:

    def __init__(self, chessboard):
        self.parent = None
        # self.kids: {(i, j): node}
        self.kids = {}
        self.chessboard = chessboard

    def getScore(self):
        chessboard = self.chessboard
        return 100 * (chessboard.count_stable_white - chessboard.count_stable_black) \
            + (chessboard.count_total_stable_direct_white
               - chessboard.count_total_stable_direct_black)


class ChessboardTree:

    def __init__(self, node):
        self.root = node
        # self.expandLayer >= 2
        self.expandLayer = 5

    def expandTree(self):
        node = self.root
        # expand the first layer
        for i, j in node.chessboard.available:
            if (i, j) not in node.kids:
                chessboard_new = setChessAI(node.chessboard, i, j)
                node_new = ChessboardTreeNode(chessboard_new)
                node.kids[(i, j)] = node_new
                node_new.parent = node

    def findBestChess(self, player):
        scores = {}
        alpha = -6400
        for key in self.root.kids:
            score = self.MaxMin(self.root.kids[key], player,
                                self.expandLayer - 1, alpha)
            scores.update({key: score})
            if alpha < score:
                alpha = score
        if not scores:
            return (-1, -1)
        max_key = max(scores, key=scores.get)
        min_key = min(scores, key=scores.get)
        return max_key

    def MaxMin(self, node, player, layer, pruning_flag):
        if layer and node.chessboard.available:
            # min layer
            if node.chessboard.offense == player:
                beta = 6400
                for i, j in node.chessboard.available:
                    if (i, j) in node.kids:
                        score = self.MaxMin(
                            node.kids[(i, j)], player, layer - 1, beta)
                    else:
                        # count += 1
                        chessboard_new = setChessAI(node.chessboard, i, j)
                        node_new = ChessboardTreeNode(chessboard_new)
                        node.kids[(i, j)] = node_new
                        node_new.parent = node
                        score = self.MaxMin(
                            node_new, player, layer - 1, beta)
                    if score <= pruning_flag:
                        beta = score
                        break
                    if beta > score:
                        beta = score
                # print('layer:', layer, 'min:', beta, 'pruning:', pruning_flag)
                return beta
            # max layer
            else:
                alpha = -6400
                for i, j in node.chessboard.available:
                    if (i, j) in node.kids:
                        score = self.MaxMin(
                            node.kids[(i, j)], player, layer - 1, alpha)
                    else:
                        # count += 1
                        chessboard_new = setChessAI(node.chessboard, i, j)
                        node_new = ChessboardTreeNode(chessboard_new)
                        node.kids[(i, j)] = node_new
                        node_new.parent = node
                        score = self.MaxMin(
                            node_new, player, layer - 1, alpha)
                    if score >= pruning_flag:
                        alpha = score
                        break
                    if alpha < score:
                        alpha = score
                # print('layer:', layer, 'max:', alpha, 'pruning:', pruning_flag)
                return alpha
        else:
            node.chessboard.updateStable()
            node.chessboard.updateCount()
            score = node.getScore()
            # print('layer:', layer, 'leaf:', node.score)
            return score


def setChessAI(chessboard, set_i, set_j):

    chessboard_new = None

    if 0 <= set_i < chessboard.row and 0 <= set_j < chessboard.col and \
            chessboard.chesses[set_i][set_j] == -1:
        # deep copy to new chessboard
        chessboard_new = chessboard.copy()
        # set chess
        chessboard_new.chesses[set_i][set_j] = chessboard.offense
        chessboard_new.offense = 3 - chessboard.offense
        # update
        chessboard_new.reverse(set_i, set_j)
        chessboard_new.updateAvailable()
        # chessboard_new.updateStable()
        chessboard_new.updateCount()

        if chessboard_new.count_available == 0:
            chessboard_new.offense = 3 - chessboard_new.offense
            chessboard_new.updateAvailable()
            # chessboard_new.updateCount()

    return chessboard_new