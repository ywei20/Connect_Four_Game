from disk import Disk
import math
import random as rnd
import sys


class GameController:
    """
    Maintains the state of the game and
    manages interaction of game elements.
    """
    def __init__(self, SPACE, filename):
        """Initialize the game controller"""
        self.SPACE = SPACE
        self.TOTAL_ROW = 6
        self.TOTAL_COL = 7
        self.WIN_NUM = 4  # when connected disks count hits 4, there is a win
        self.diam = self.SPACE['w']/self.TOTAL_COL  # diameter of each disk
        self.disk_count = 0  # keep track of how many disks in the board
        self.isRed = 1  # mark whether it is red disk'turn
        self.last_filled_col = -1  # record column index last filled
        self.last_filled_row = -1  # record row index last filled
        self.board = [[None]*self.TOTAL_COL for _ in range(self.TOTAL_ROW)]
        self.disks_per_col = [0 for _ in range(self.TOTAL_COL)]  # disks/col
        self.win = False  # if one side win, change it to true
        self.tie = False  # if no one wins and the board's full, change to True
        self.record = False  # after recording current score, change to True
        self.countdown = 80  # set delay for computer move
        self.filename = filename

    def prepare_to_drop(self, cur_x, cur_y):
        """draw a disk at the column corresponding to x,y coordinate"""
        # get column index to drop a disk:
        col_idx = int(math.floor(cur_x / self.diam))

        # if it is player's turn and valid, display a disk at desired location
        if self.isRed and self.valid_to_drop(cur_y, col_idx):
            new_disk = Disk(self.SPACE, self.TOTAL_ROW, col_idx,
                            self.disks_per_col[col_idx],
                            self.isRed, self.diam)
            new_disk.draw_me()

    def start_drop(self, cur_x, cur_y):
        """add a disk to the board according to x,y coordinate"""
        col_idx = int(math.floor(cur_x / self.diam))
        if self.isRed and self.valid_to_drop(cur_y, col_idx):
            self.drop_a_disk(col_idx)

    def update(self):
        """Update game state on every frame"""
        # traverse board and display all disks
        for col in self.board:
            for disk in col:
                if disk is None:
                    continue
                disk.display()  # display all disks on board

        self.display_frame()  # display frame

        # display whose turn it is
        if not self.win and not self.tie and self.is_last_disk_land():
            if self.isRed:
                RED = (0.8, 0.2, 0.2)
                fill(*RED)
                textSize(20)
                textAlign(LEFT)
                text("Red's Turn", 0, 20)
            else:
                YELLOW = (1.0, 1.0, 0)
                fill(*YELLOW)
                textSize(20)
                textAlign(RIGHT)
                text("Yellow's Turn", self.SPACE['w'], 20)

        # if it's the computer's turn and there is not a win or tie yet
        if not self.isRed and not self.win and not self.tie:
            self.computer_make_move()  # computer make a move

        # once the last disk lands, check game status
        if self.is_last_disk_land() and (self.win or self.tie):
            self.display_game_end_message()  # display game end info
            if not self.record:
                self.countdown -= 2
                if self.countdown == 0:
                    self.record_score()  # ask for user name
                    self.record = True
            if self.record:  # ask for a choice after recording
                fill(1)
                textSize(40)
                textAlign(CENTER)
                text("Play Again? Y / N ", self.SPACE['w']/2,
                     self.SPACE['h']/2 + 100)

    def display_frame(self):
        """display frames"""
        # top left corner of board
        x1, y1 = 0, (self.SPACE['h'] - self.TOTAL_ROW * self.diam)
        x2, y2 = 0, self.SPACE['h']  # left bottom corner of board
        x3, y3 = self.SPACE['w'], self.SPACE['h']  # right bottom corner
        stroke(0, 0.2, 0.8)
        strokeWeight(20)

        # draw vertical frames
        for i in range(self.TOTAL_COL + 1):
            line(x1+i*self.diam, y1, x2+i*self.diam, y2)
        # draw horizontal frames
        for i in range(self.TOTAL_ROW + 1):
            line(x2, y2-i*self.diam, x3, y3-i*self.diam)

    def display_game_end_message(self):
        """display appropriate messages to show how game ends"""
        noStroke()
        fill(0, 0.65)  # set transparent fill parameter
        rect(self.diam, self.diam*2, self.diam*5, self.diam*4)
        if self.win and self.isRed:  # user wins
            fill(1)
            textSize(50)
            textAlign(CENTER)
            text("RED WINS!", self.SPACE['w']/2, self.SPACE['h']/2 - 50)
        elif self.win:  # computer wins
            fill(1)
            textSize(50)
            textAlign(CENTER)
            text("YELLOW WINS!", self.SPACE['w']/2, self.SPACE['h']/2 - 50)
        else:  # a tie
            fill(1)
            textSize(50)
            textAlign(CENTER)
            text("Game Over!", self.SPACE['w']/2, self.SPACE['h']/2 - 50)

    def valid_to_drop(self, cur_y, col_idx):
        """return whether it is valid to drop a ball"""
        # if there is a win or tie, return false
        if self.win or self.tie:
            return False
        # if mouse position is below the upper bound of board, return false
        if cur_y > self.SPACE['h'] - self.TOTAL_ROW*self.diam:
            return False
        # if the column is full, return false
        if self.disks_per_col[col_idx] >= self.TOTAL_ROW:
            return False
        # if the last disk has not landed, return false
        return self.is_last_disk_land()

    def is_last_disk_land(self):
        """return whether the last falling disk has landed"""
        if self.last_filled_row >= 0:
            last_disk = self.board[self.last_filled_row][self.last_filled_col]
            if last_disk.y < last_disk.lowest_point:
                return False
        return True

    def computer_make_move(self):
        """computer picks a position to drop a disk"""
        self.countdown -= 1
        if self.countdown == 0:
            # make a new 6 x 7 board easier for score calculation
            score_board = self.get_board()
            # pick by non-minimax method(code comment out)
            # col_idx = self.pick_best_move(score_board, self.isRed)

            col_idx = self.minimax(score_board, 3, -sys.maxsize,
                                   sys.maxsize, True)[0]
            # print(col_idx)
            self.drop_a_disk(col_idx)
            self.countdown = 80  # reset countdown to initial value

    def drop_a_disk(self, col_idx):
        """drop a disk of the appropriate color to the board"""
        # calculate the target slot's row index
        row_idx = self.TOTAL_ROW - 1 - self.disks_per_col[col_idx]
        # generate a new disk instance
        new_disk = Disk(self.SPACE, self.TOTAL_ROW, col_idx,
                        self.disks_per_col[col_idx], self.isRed, self.diam)
        self.board[row_idx][col_idx] = new_disk
        self.last_filled_col = col_idx  # update last filled col to this col
        self.last_filled_row = row_idx  # update last filled row to this row
        self.disks_per_col[col_idx] += 1  # add num of disks of col_idx by 1
        self.disk_count += 1  # increase total disk counts by 1
        board = self.get_board()
        if self.is_win_move(board, self.isRed):
            self.win = True
        if not self.win and self.disk_count == self.TOTAL_ROW * self.TOTAL_COL:
            self.tie = True
        if not self.win and not self.tie:
            self.isRed = 1 - self.isRed  # switch isRed boolean to the opposite

    def is_win_move(self, board, side):
        """check whether the move (row, col) creates a win for player 'side'
        @parameters:
        board: a 6 x 7 matrix of int, composed of -1(empty), 1(user), 0(AI)
        side: 1 stands for user(red disk), 0 stands for AI(yellow disk)
        @return: true if there is win, else false"""
        return self.col_win(board, side) or self.row_win(board, side) or\
            self.pos_diag_win(board, side) or self.neg_diag_win(board, side)

    def col_win(self, board, side):
        """check columns, return true if see a win else return false"""
        for col in range(self.TOTAL_COL):
            col_array = [line[col] for line in board]
            for row in range(self.TOTAL_ROW//2):
                window = col_array[row:row+self.WIN_NUM]
                if window.count(side) == self.WIN_NUM:
                    return True
        return False

    def row_win(self, board, side):
        """check current row, return true if see a win else return false"""
        for row in range(self.TOTAL_ROW):
            for col in range(self.TOTAL_COL//2+1):
                window = board[row][col:col+self.WIN_NUM]
                if window.count(side) == self.WIN_NUM:
                    return True
        return False

    def pos_diag_win(self, board, side):
        """check diagonals with positive slope, return win if see one"""
        for row in range(self.TOTAL_ROW//2):
            for col in range(self.TOTAL_COL//2, self.TOTAL_COL):
                window = [board[row+i][col-i] for i in range(self.WIN_NUM)]
                if window.count(side) == self.WIN_NUM:
                    return True
        return False

    def neg_diag_win(self, board, side):
        """check diagonals with negative slope, return win if see one"""
        for row in range(self.TOTAL_ROW//2):
            for col in range(self.TOTAL_COL//2+1):
                window = [board[row+i][col+i] for i in range(self.WIN_NUM)]
                if window.count(side) == self.WIN_NUM:
                    return True
        return False

    def get_board(self):
        """make a board for score calculation based on self.board
        return a board with -1 for none, 1 for red disk , 0 for yellow disk"""
        board = [[-1 if self.board[r][c] is None else self.board[r][c].isRed
                 for c in range(self.TOTAL_COL)]
                 for r in range(self.TOTAL_ROW)]
        return board

    def get_valid_columns(self, board):
        """return a list of column index that are not full"""
        cols_open_for_disk = []
        EMPTY = -1
        for col in range(len(board[0])):
            if board[0][col] == EMPTY:
                cols_open_for_disk.append(col)
        return cols_open_for_disk

    def get_open_row(self, board, col):
        """return the lowest row index of the col that are open for a disk"""
        EMPTY = -1
        for row in range(len(board)-1, -1, -1):
            if board[row][col] == EMPTY:
                return row

    def score_window(self, window, side):
        """calculate score of a subarray of length 4 for player 'side',
        return a score for whoever 'side' stands for.
        @parameter: window is a list of int of length 4
            side is 1 or 0, 1 stands for red disk, 0 stands for yellow(AI)"""
        EMPTY = -1  # -1 stands for an empty cell
        oppo_side = 1 - side  # opposite side
        score = 0
        # Offense Stratigies
        if window.count(side) == 4:
            score += 100
        elif window.count(side) == 3 and window.count(EMPTY) == 1:
            score += 5
        elif window.count(side) == 2 and window.count(EMPTY) == 2:
            score += 2
        # Defense Strategies
        if window.count(oppo_side) == 3 and window.count(EMPTY) == 1:
            score -= 80
        elif window.count(oppo_side) == 2 and window.count(EMPTY) == 2:
            score -= 2
        elif window.count(oppo_side) == 1 and window.count(EMPTY) == 3:
            score -= 1
        return score

    def score_position(self, board, side):
        """calculate score of a board for the player 'side',
        return a score for whoever 'side' stands for.
        @parameter: board is a list of list of int, with size 6 x 7
            side is 1 or 0, 1 stands for red disk, 0 stands for yellow(AI)"""
        score = 0
        n = len(board)
        m = len(board[0])

        # for each column, score vertical windows
        for col in range(m):
            col_array = [item[col] for item in board]
            # col_count = col_array.count(side)
            # score += col_count * (3 - abs(m//2 - col))
            for row in range(n//2):
                window = col_array[row:row+self.WIN_NUM]
                score += self.score_window(window, side)

        # score horizontal windows
        for row in range(n):
            for col in range(m//2+1):
                window = board[row][col:col+self.WIN_NUM]
                score += self.score_window(window, side)

        # score positive diagonal windows
        for row in range(n//2):
            for col in range(m//2, m):
                window = [board[row+i][col-i] for i in range(self.WIN_NUM)]
                score += self.score_window(window, side)

        # score negative diagonal windows
        for row in range(n//2):
            for col in range(m//2+1):
                window = [board[row+i][col+i] for i in range(self.WIN_NUM)]
                score += self.score_window(window, side)

        return score

    # def pick_best_move(self, board, side):
    #     """given a board , return a col with highest score for the side
    #     An alternative AI algorithm besides minimax"""
    #     valid_columns = self.get_valid_columns(board)
    #     best_score = -sys.maxsize
    #     best_col = rnd.choice(valid_columns)
    #     for col in valid_columns:
    #         row = self.get_open_row(board, col)
    #         new_board = [[board[r][c] for c in range(len(board[0]))]
    #                      for r in range(len(board))]
    #         new_board[row][col] = side
    #         new_score = self.score_position(new_board, side)

    #         if new_score > best_score:
    #             best_score = new_score
    #             best_col = col
    #     return best_col

    def minimax(self, board, depth, alpha, beta, maximizing):
        """gives the best move given current board
        @parameters:
        board: a 6 x 7 matrix of int, composed of -1(empty), 1(user), 0(AI)
        depth: int, > 0, the larger the deeper recursion goes down to
        side: 0 stands for AI(yellow disk), 1 stands for user(red)
        alpha: score for the current side, alpha always get maximized
        beta: score for the opposite side, beta always get minimized
        maximizing: True means maximizing; False means minimizing
        @return: (col_index, score of board)"""
        EMPTY = -1
        HUMAN = 1
        AI = 0
        if self.is_win_move(board, AI):  # this side wins
            return (None, 1000000)
        elif self.is_win_move(board, HUMAN):  # opponent wins
            return (None, -1000000)
        elif sum(r.count(EMPTY) for r in board) == 0:  # a draw
            return (None, 0)
        elif depth == 0:
            return (None, self.score_position(board, AI))

        valid_columns = self.get_valid_columns(board)
        if maximizing:  # maximizing player
            best_score = -sys.maxsize
            best_col = rnd.choice(valid_columns)
            for new_col in valid_columns:
                new_row = self.get_open_row(board, new_col)
                new_board = [[board[r][c] for c in range(len(board[0]))]
                             for r in range(len(board))]
                new_board[new_row][new_col] = AI
                new_score = self.minimax(new_board, depth-1,
                                         alpha, beta, False)[1]
                if new_score > best_score:
                    best_score = new_score
                    best_col = new_col
                alpha = max(alpha, best_score)
                if beta <= alpha:
                    break
            return best_col, best_score

        else:  # minimizing player
            best_score = sys.maxsize
            best_col = rnd.choice(valid_columns)
            for new_col in valid_columns:
                new_row = self.get_open_row(board, new_col)
                new_board = [[board[r][c] for c in range(len(board[0]))]
                             for r in range(len(board))]
                new_board[new_row][new_col] = HUMAN
                new_score = self.minimax(new_board, depth-1,
                                         alpha, beta, True)[1]
                if new_score < best_score:
                    best_score = new_score
                    best_col = new_col
                beta = min(beta, best_score)
                if beta <= alpha:
                    break
            return best_col, best_score

    def record_score(self):
        # name = self.input("Enter your name please: ")
        # if self.win and self.isRed:  # if the user wins, update scores
        #     scores = {}
        #     with open(self.filename, "r+") as f:
        #         for line in f:
        #             data = line.strip().split()
        #             print(data)
        #             scores[data[0]] = int(data[1])
        #         print(scores)
        #         if name in scores.keys():
        #             scores[name] += 1
        #         else:
        #             scores[name] = 1
        #         ranks = sorted(scores.items(),
        #                        key=lambda x: x[1],
        #                        reverse=True)
        #         print(ranks)
        #         contents = ''.join([i[0] + ' ' + str(i[1]) + '\n'
        #                             for i in ranks])
        #         f.seek(0)  # change the position to the beginning
        #         f.truncate()  # erase original content
        #         f.write(contents)
        pass

    def input(self, message=''):
        from javax.swing import JOptionPane
        return JOptionPane.showInputDialog(frame, message)
