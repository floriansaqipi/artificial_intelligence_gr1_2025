#!/usr/bin/env python3

from sys import argv
from blockednqueens import BlockedNQueens

hr = "=" * 80

if __name__ == "__main__": 
    
    N = int(argv[1])
    blocked_cells = []

    for arg in argv[2:]:
        try:
            i = int(arg[0])
            j = int(arg[1])
            if 1<=i<=8 and 1<=j<=8:
                blocked_cells.append((i, j))
            else:
                print(f"Gabim: i={i} ose j={j} janë jasht intervalit 1-8.")
                exit(2)
        except ValueError:
            print(f"Gabim: i={arg[1]} ose j={arg[0]} nuk janë numra valid.")
            exit(1)

    print(f"N: {N}")
    print("Qelizat e bllokuara:")
    for cell in blocked_cells:
        print(f"\t{cell}")

    board = BlockedNQueens(N, blocked_cells)

    print(f"{hr}\nTabela para zgjidhjes:\n{board}\n{hr}\n")
    
    board = board.solve()
    
    print(f"\n{hr}\nTabela pas zgjidhjes:\n{board}\n{hr}\n")
