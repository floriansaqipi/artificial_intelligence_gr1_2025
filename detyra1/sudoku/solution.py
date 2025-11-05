from sudoku_board import SudokuBoard
from collections import deque
from copy import deepcopy
import traceback

def bfs_with_pruning(board: SudokuBoard) -> SudokuBoard:
    root = deepcopy(board)
    queue = deque()

    queue.append(root)
    counter = 1
    while queue:
        current_state = queue.popleft()
        coords = current_state.next_coords()

        if coords is None:
            break

        next_x, next_y = coords
        
        for val in range (1,10):
            next_state = deepcopy(current_state)
            try:
                next_state.set_cell(next_x, next_y, val)
                queue.append(next_state)
            except Exception as e:
                continue

    return current_state
