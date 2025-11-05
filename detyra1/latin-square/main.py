#!/usr/bin/env python3

import time
from sys import argv
from utils import print_latin_square
from latin_square import iddfs_solve_latin_square
    
if __name__ == "__main__":
    start = time.time()
    n = int(argv[1]) if len(argv) > 1 else 3
    solutions = iddfs_solve_latin_square(n)
    end = time.time()

    print(f'Koha totale e ekzekutimit: {end - start:.4f} sekonda.')
