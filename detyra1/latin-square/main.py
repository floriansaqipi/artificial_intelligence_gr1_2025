#!/usr/bin/env python3

from sys import argv
from utils import print_latin_square
from latin_square import iddfs_solve_latin_square
    
if __name__ == "__main__":
    n = int(argv[1]) if len(argv) > 1 else 3
    solutions = iddfs_solve_latin_square(n)
    # for i, sol in enumerate(solutions):
    #     print(f"Solution {i + 1}:")
    #     print_latin_square(sol)
    #     print()
