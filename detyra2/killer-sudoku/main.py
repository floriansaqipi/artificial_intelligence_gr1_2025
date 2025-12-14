#!/usr/bin/env python3

from sys import argv
from killersudoku import KillerSudoku

difficulty = argv[1] if len(argv) > 1
if difficulty != "easy" \
    and difficulty != "medium" \
    and difficulty != "hard" \
    and difficulty != "expert":
    print("\nPërdorimi: ./main.py [vështirësia]")
    print("\nNivelet e vështirësisë: easy, medium, hard, expert")
    print("\n\n\tp.sh.: ./main.py hard")
    exit(0)

board = KillerSudoku.fetchBoard(difficulty=difficulty)

print(f"Tabela para zgjidhjes:\n{board}\n")

solved = killer_sudoku_board.solve()

print(f"Tabela pas zgjidhjes:\n{board}\n")
