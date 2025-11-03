def print_latin_square(latin_square):
    width = len(str(max(max(latin_square, key=max))))
    for row in latin_square:
        print(" ".join(str(x).rjust(width) for x in row))

def find_empty_cell(grid, n):
    for i in range(n):
        for j in range(n):
            if grid[i][j] is None:
                return i, j
    return None, None

def is_valid(grid, n, r, c, val):
    for j in range(n):
        if grid[r][j] == val:
            return False
    for i in range(n):
        if grid[i][c] == val:
            return False
            
    return True