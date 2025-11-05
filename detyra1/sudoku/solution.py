from sudoku_board import SudokuBoard
from collections import deque

def bfs_with_pruning(board: SudokuBoard) -> SudokuBoard:
    root_state = board
    queue = deque()
    queue.append(root_state)
    while queue:
        current_state = queue.popleft()

        if not is_valid(current_state):
            continue # prune dat shiiiihhhh
       
        

        for move in current_state.next_moves():
            queue.append(move)
