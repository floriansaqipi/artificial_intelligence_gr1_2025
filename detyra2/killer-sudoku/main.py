#!/usr/bin/env python3

from sys import argv
import json
from killersudoku import KillerSudoku

def get_board(difficulty) -> dict:
    if difficulty != "easy": \
        and difficulty != "medium" \
        and difficulty != "hard" \
        and difficulty != "expert":
        print("\nPërdorimi: ./main.py [vështirësia]")
        print("\nNivelet e vështirësisë: easy, medium, hard, expert")
        print("\n\n\tp.sh.: ./main.py hard")
        exit(0) 

    with open(f"data/{difficulty}.json", "r") as file:
        return json.load(file)

if __name__ == "__main__":
    difficulty = argv[1] if len(argv) > 1 else "easy"

    print(f"Vështirësia: {difficulty}")

    board_dict = get_board(difficulty)

    board = KillerSudoku.fetch_board(board_dict)

    print(f"Tabela para zgjidhjes:\n{board}\n")

    solved = board.solve()

    print(f"Tabela pas zgjidhjes:\n{board}\n")
