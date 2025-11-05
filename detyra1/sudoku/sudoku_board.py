class SudokuBoard:
    def __init__(self, grid=None):
        if grid:
            if len(grid) != 9 or any(len(row) != 9 for row in grid):
                raise ValueError("Grid must be 9x9.")
            self.grid = [list(row) for row in grid]
        else:
            self.grid = [[0 for _ in range(9)] for _ in range(9)]
        self.last_row = 1
        self.last_col = 1

    def set_cell(self, row, col, value):
        if not (1 <= row <= 9 and 1 <= col <= 9):
            raise ValueError("Rreshti dhe kolona duhet te jene mes 1 dhe 9")
        if not (0 <= value <= 9):
            raise ValueError(f"Vlera {value} eshte jasht intervalit [0-9].")
        
        if value in self.grid[row-1]:
            raise ValueError(f"Vlera {value} eksiston ne rreshtin {row}")

        for r in range(1, len(self.grid)+1):
            if value == self.get_cell(r,col):
                raise ValueError(f"Vlera {value} ekziston ne kolonën {col}")

        big_row = (row - 1) // 3
        big_col = (col - 1) // 3

        for i in range (1,4):
            for j in range (1,4):
                if self.get_cell(big_row * 3 + i, big_col * 3 + j) == value:
                    raise ValueError(f"Vlera ekziston ne sub-katrorin {big_row * 3 + big_col}")

        self.grid[row - 1][col - 1] = value

    def get_cell(self, row, col):
        if not (1 <= row <= 9 and 1 <= col <= 9):
            raise ValueError(f"Row and column must be between 1 and 9. They are {row} and {col}")
        return self.grid[row-1][col-1]

    def next_coords(self):
        #for i in range (self.last_row, 10):
        #    for j in range (self.last_col, 10):
        for i in range (1, 10):
            for j in range (1, 10):
               if self.get_cell(i, j) == 0:
                    self.last_row = i
                    self.last_col = j
                    return i, j
        return None

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
