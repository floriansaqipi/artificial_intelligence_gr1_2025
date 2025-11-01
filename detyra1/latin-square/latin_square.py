def solve_latin_square(latin_square, n):

    for i in range(n):
        for j in range(n):
            latin_square[i][j] = (i + j) % n + 1

    return latin_square