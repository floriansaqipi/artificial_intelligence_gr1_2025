#!/usr/bin/env python3

from sys import argv
from utils import print_latin_square
from latin_square import solve_latin_square

def main(n):
    latin_square = [[0] * n for _ in range(n)]
    solve_latin_square(latin_square, n)
    print_latin_square(latin_square)
    
if __name__ == "__main__":
    n = int(argv[1]) if len(argv) > 1 else 5
    main(n)