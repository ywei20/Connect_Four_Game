from game_controller import GameController
from disk import Disk
import sys

SPACE = {'w': 700, 'h': 700}
filename = "scores.txt"
HUMAN = 1
AI = 0


def test_constructor():
    gc = GameController(SPACE, filename)

    assert gc.SPACE['w'] == 700 and gc.SPACE['h'] == 700 and \
        gc.filename == filename and hasattr(gc, "diam") and \
        hasattr(gc, "disk_count") and hasattr(gc, "isRed") and \
        hasattr(gc, "last_filled_col") and hasattr(gc, "countdown") and \
        hasattr(gc, "last_filled_row") and \
        gc.diam == gc.SPACE['w'] / gc.TOTAL_COL and \
        not gc.win and not gc.tie and not gc.record and \
        len(gc.board) == gc.TOTAL_ROW and \
        len(gc.board[0]) == gc.TOTAL_COL and gc.board[0][0] is None and \
        len(gc.disks_per_col) == gc.TOTAL_COL and gc.disks_per_col[0] == 0


def test_start_drop():
    gc = GameController(SPACE, filename)
    cur_x, cur_y = 300, 30
    num_empty_cells_bef = sum(row.count(None) for row in gc.board)
    gc.start_drop(cur_x, cur_y)
    num_empty_cells_aft = sum(row.count(None) for row in gc.board)
    assert num_empty_cells_aft == num_empty_cells_bef - 1


def test_drop_a_disk():
    gc = GameController(SPACE, filename)
    gc.disks_per_col = [0, 1, 2, 0, 0, 0, 0]
    col_idx = 2
    row_idx = gc.TOTAL_ROW - 1 - gc.disks_per_col[col_idx]
    num_empty_cells_bef = sum(row.count(None) for row in gc.board)
    disk_count_bef = gc.disk_count
    gc.drop_a_disk(col_idx)
    num_empty_cells_aft = sum(row.count(None) for row in gc.board)
    disk_count_aft = gc.disk_count
    assert num_empty_cells_aft == num_empty_cells_bef - 1 and \
        gc.last_filled_col == col_idx and \
        gc.last_filled_row == row_idx and \
        gc.disks_per_col[col_idx] == 3 and \
        disk_count_aft == disk_count_bef + 1


def test_valid_to_drop():
    gc1 = GameController(SPACE, filename)
    gc2 = GameController(SPACE, filename)

    gc1.win = True
    gc1.tie = True
    cur_y = 200
    col_idx = 0
    assert not gc1.valid_to_drop(cur_y, col_idx)
    assert not gc2.valid_to_drop(cur_y, col_idx)

    cur_y = 10
    assert gc2.valid_to_drop(cur_y, col_idx)

    gc2.disks_per_col[0] = 6
    assert not gc2.valid_to_drop(cur_y, col_idx)


def test_computer_make_move():
    gc = GameController(SPACE, filename)
    countdown_bef = gc.countdown
    gc.computer_make_move()
    countdown_aft = gc.countdown
    assert countdown_aft == countdown_bef - 1

    gc.countdown = 1
    gc.computer_make_move()
    assert gc.countdown == 80


def test_is_last_disk_land():
    gc = GameController(SPACE, filename)
    assert gc.is_last_disk_land()


def test_col_win():
    gc = GameController(SPACE, filename)
    board = [[-1, -1, -1, -1, -1, -1, -1],
             [-1, -1, -1, -1, -1, -1, -1],
             [-1, -1, -1, -1, -1, -1, -1],
             [-1, -1,  1,  0, -1, -1, -1],
             [-1,  1,  1,  0, -1, -1, -1],
             [-1,  0,  1,  0, -1, -1, -1]]
    assert not gc.col_win(board, HUMAN)
    assert not gc.col_win(board, AI)
    board[2][2] = 1
    assert gc.col_win(board, HUMAN)


def test_row_win():
    gc = GameController(SPACE, filename)
    board = [[-1, -1, -1, -1, -1, -1, -1],
             [-1, -1, -1, -1, -1, -1, -1],
             [-1, -1, -1, -1, -1, -1, -1],
             [-1,  0,  0,  0, -1, -1, -1],
             [-1,  1,  1,  1, -1, -1, -1],
             [-1,  0,  1,  0,  1, -1, -1]]
    assert not gc.row_win(board, HUMAN)
    assert not gc.row_win(board, AI)
    board[4][4] = 1
    assert gc.row_win(board, HUMAN)


def test_pos_diag_win():
    gc = GameController(SPACE, filename)
    board = [[-1, -1, -1, -1, -1, -1, -1],
             [-1, -1, -1, -1, -1, -1, -1],
             [-1, -1, -1, -1, -1, -1, -1],
             [-1,  0,  0,  0,  1, -1, -1],
             [-1,  1,  1,  1,  0, -1, -1],
             [-1,  0,  1,  0,  1, -1, -1]]
    assert not gc.pos_diag_win(board, HUMAN)
    assert not gc.pos_diag_win(board, AI)
    board[5][5] = 0
    board[4][5] = 1
    board[3][5] = 0
    board[2][5] = 1
    assert gc.pos_diag_win(board, HUMAN)


def test_neg_diag_win():
    gc = GameController(SPACE, filename)
    board = [[-1, -1, -1, -1, -1, -1, -1],
             [-1, -1, -1, -1, -1, -1, -1],
             [-1, -1, -1, -1, -1, -1, -1],
             [-1,  0,  0,  0,  1, -1, -1],
             [-1,  1,  1,  1,  0, -1, -1],
             [-1,  0,  1,  0,  1, -1, -1]]
    assert not gc.neg_diag_win(board, HUMAN)
    assert not gc.neg_diag_win(board, AI)
    board[2][3] = 1
    board[5][5] = 0
    board[4][5] = 1
    board[2][2] = 0
    assert gc.neg_diag_win(board, AI)


def test_is_win_move():
    gc = GameController(SPACE, filename)
    board = [[-1, -1, -1, -1, -1, -1, -1],
             [-1, -1, -1, -1, -1, -1, -1],
             [-1, -1, -1, -1, -1, -1, -1],
             [-1,  0,  0,  0, -1, -1, -1],
             [-1,  1,  1,  1, -1, -1, -1],
             [-1,  0,  1,  0,  1, -1, -1]]
    assert not gc.is_win_move(board, HUMAN)
    assert not gc.is_win_move(board, AI)
    board[4][4] = 1
    assert gc.is_win_move(board, HUMAN)


def test_get_board():
    gc = GameController(SPACE, filename)
    board = [[-1, -1, -1, -1, -1, -1, -1],
             [-1, -1, -1, -1, -1, -1, -1],
             [-1, -1, -1, -1, -1, -1, -1],
             [-1, -1, -1, -1, -1, -1, -1],
             [-1, -1, -1, -1, -1, -1, -1],
             [-1, -1, -1, -1, -1, -1, -1]]
    assert gc.get_board() == board

    col_idx = 0
    disk = Disk(gc.SPACE, gc.TOTAL_ROW, col_idx,
                gc.disks_per_col[col_idx],
                gc.isRed, gc.diam)
    disk.isRed = 1 - disk.isRed
    gc.board[5][3] = disk
    board[5][3] = 0
    assert gc.get_board() == board


def test_get_valid_columns():
    gc = GameController(SPACE, filename)
    board = [[-1, -1,  1,  1, -1, -1, -1],
             [-1, -1,  0,  0, -1, -1, -1],
             [-1,  1,  0,  1, -1, -1, -1],
             [-1,  0,  0,  0, -1, -1, -1],
             [-1,  1,  1,  1, -1, -1, -1],
             [-1,  0,  1,  0,  1, -1, -1]]
    assert gc.get_valid_columns(board) == [0, 1, 4, 5, 6]


def test_get_open_row():
    gc = GameController(SPACE, filename)
    board = [[-1, -1,  1,  1, -1, -1, -1],
             [-1, -1,  0,  0, -1, -1, -1],
             [-1,  1,  0,  1, -1, -1, -1],
             [-1,  0,  0,  0, -1, -1, -1],
             [-1,  1,  1,  1, -1, -1, -1],
             [-1,  0,  1,  0,  1, -1, -1]]
    col0 = 0
    col1 = 1
    col4 = 4
    assert gc.get_open_row(board, col0) == 5
    assert gc.get_open_row(board, col1) == 1
    assert gc.get_open_row(board, col4) == 4


def test_score_window():
    gc = GameController(SPACE, filename)
    window0 = [1,  1,  1,  1]
    window1 = [-1, -1, -1, -1]
    window2 = [1, -1,  1,  1]
    window3 = [-1,  1,  1, -1]
    assert gc.score_window(window0, HUMAN) == 100
    assert gc.score_window(window1, HUMAN) == 0
    assert gc.score_window(window1, AI) == 0
    assert gc.score_window(window2, HUMAN) == 5
    assert gc.score_window(window2, AI) == -80
    assert gc.score_window(window3, HUMAN) == 2
    assert gc.score_window(window3, AI) == -2


def test_score_position():
    gc = GameController(SPACE, filename)
    board = [[-1, -1, -1, -1, -1, -1, -1],
             [-1, -1, -1, -1, -1, -1, -1],
             [-1, -1, -1, -1, -1, -1, -1],
             [-1, -1,  1,  0, -1, -1, -1],
             [-1,  1,  1,  0, -1, -1, -1],
             [-1,  0,  1,  0, -1, -1, -1]]
    assert gc.score_position(board, HUMAN) == -81
    assert gc.score_position(board, AI) == -82


def test_minimax():
    gc = GameController(SPACE, filename)
    board = [[-1, -1, -1, -1, -1, -1, -1],
             [-1, -1, -1, -1, -1, -1, -1],
             [-1, -1, -1, -1, -1, -1, -1],
             [-1, -1, -1,  0, -1, -1, -1],
             [-1, -1, -1,  1,  0, -1, -1],
             [-1, -1,  0,  1,  1, -1,  1]]
    depth = 3
    alpha = -sys.maxsize
    beta = sys.maxsize
    maximizing = True
    best_col = gc.minimax(board, depth, alpha, beta, maximizing)[0]
    assert best_col == 5
