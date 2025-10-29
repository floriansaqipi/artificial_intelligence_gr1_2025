class SudokuBoard:
    def __init__(self, grid=None):
        if grid:
            if len(grid) != 9 or any(len(row) != 9 for row in grid):
                raise ValueError("Grid must be 9x9.")
            self.grid = [list(row) for row in grid]
        else:
            self.grid = [[0 for _ in range(9)] for _ in range(9)]

    def set_cell(self, row, col, value):
        if not (0 <= row < 9 and 0 <= col < 9):
            raise ValueError("Row and column must be between 0 and 8.")
        if not (0 <= value <= 9):
            raise ValueError("Value must be between 0 and 9.")
        self.grid[row][col] = value

    def get_cell(self, row, col):
        if not (0 <= row < 9 and 0 <= col < 9):
            raise ValueError("Row and column must be between 0 and 8.")
        return self.grid[row][col]

    def reset(self):
        """Reset the board to all zeros."""
        self.grid = [[0 for _ in range(9)] for _ in range(9)]

    def __str__(self):
        lines = ["+-------+-------+-------+"]
        for i, row in enumerate(self.grid):
            line = "| "
            for j, val in enumerate(row):
                cell = str(val) if val != 0 else "."
                line += cell + " "
                if (j + 1) % 3 == 0:
                    line += "| "
            lines.append(line)
            if (i + 1) % 3 == 0:
                lines.append("+-------+-------+-------+")
        return "\n".join(lines)

if __name__ == "__main__":
    example_grid = [
        [5, 3, 0, 0, 7, 0, 0, 0, 0],
        [6, 0, 0, 1, 9, 5, 0, 0, 0],
        [0, 9, 8, 0, 0, 0, 0, 6, 0],
        [8, 0, 0, 0, 6, 0, 0, 0, 3],
        [4, 0, 0, 8, 0, 3, 0, 0, 1],
        [7, 0, 0, 0, 2, 0, 0, 0, 6],
        [0, 6, 0, 0, 0, 0, 2, 8, 0],
        [0, 0, 0, 4, 1, 9, 0, 0, 5],
        [0, 0, 0, 0, 8, 0, 0, 7, 9],
    ]

    board = SudokuBoard(example_grid)
    print(board)

    board.set_cell(0, 2, 4)
    print("\nAfter setting cell (0, 2) to 4:\n")
    print(board)
