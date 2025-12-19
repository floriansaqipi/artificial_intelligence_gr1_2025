#!/usr/bin/env python3

from sys import argv
from blockednqueens import BlockedNQueens
from shutil import get_terminal_size as gts

hr = "=" * gts().columns

if __name__ == "__main__": 
    
    N = int(argv[1])
    blocked_cells = []

    for arg in argv[2:]:
        try:
            i = int(arg[0]) - 1
            j = int(arg[1]) - 1
            
            if (i,j) in blocked_cells:
                continue
           
            elif 0<=i<=N-1 and 0<=j<=N-1: 
                blocked_cells.append((i, j))
            
            else:
                print(f"Gabim: i={i+1} ose j={j+1} janë jasht intervalit [1-{N}].")
                exit(2)
        except ValueError:
            print(f"Gabim: i={arg[1]} ose j={arg[0]} nuk janë numra valid.")
            exit(1)

    board = BlockedNQueens(
                blocked_cells=blocked_cells,
                N=N,
            )

    print(f"\n{hr}\n\nTabela para zgjidhjes:\n\n{board}\n\n{hr}\n\n")
    
    if not board.solve():
        print(f"\n{hr}\n\nTABELA NUK KA ZGJIDHJE! - Deri qitu kemi mrri:\n")
    else:
        print(f"\n{hr}\n\nTabela pas zgjidhjes:\n")

    print(f"{board}\n\n{hr}\n")
