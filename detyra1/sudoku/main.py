#!/usr/bin/env python3

from sys import argv
from sudoku_board import SudokuBoard
from solution import bfs_with_pruning

def main(board: SudokuBoard) -> SudokuBoard:
    print("duke zgjidhur sudoku me bfs...\n") 
    board = bfs_with_pruning(board) 
    return board

if __name__ == "__main__":
    easy_grid = [
        [8, 3, 0, 0, 0, 0, 0, 5, 1],
        [0, 9, 0, 0, 0, 0, 4, 8, 2],
        [7, 0, 5, 1, 2, 0, 6, 0, 0],
        [3, 0, 0, 6, 0, 0, 5, 1, 0],
        [0, 2, 9, 8, 1, 5, 3, 6, 0],
        [0, 6, 0, 7, 3, 0, 8, 0, 0],
        [9, 0, 0, 3, 0, 0, 0, 0, 0],
        [0, 5, 7, 4, 6, 0, 0, 0, 0],
        [0, 0, 3, 0, 8, 0, 9, 4, 0],
    ]

    medium_grid = [
        [9, 0, 2, 0, 0, 1, 8, 0, 0],
        [6, 4, 0, 5, 0, 8, 0, 0, 0],
        [0, 0, 0, 4, 0, 0, 0, 0, 7],
        [4, 1, 0, 3, 2, 0, 7, 8, 9],
        [3, 5, 9, 8, 1, 0, 6, 4, 0],
        [0, 0, 0, 9, 6, 0, 0, 0, 5],
        [5, 0, 4, 0, 0, 0, 0, 7, 1],
        [0, 2, 0, 0, 0, 9, 0, 0, 0],
        [0, 0, 0, 1, 0, 0, 4, 2, 0],
    ]

    hard_grid = [
        [0, 7, 9, 0, 8, 0, 0, 0, 0],
        [0, 0, 8, 0, 1, 0, 0, 6, 4],
        [0, 6, 0, 0, 0, 0, 5, 0, 0],
        [6, 8, 7, 3, 0, 2, 9, 0, 5],
        [9, 1, 3, 0, 0, 0, 0, 0, 0],
        [0, 0, 4, 0, 0, 7, 0, 0, 0],
        [0, 0, 3, 0, 0, 0, 0, 0, 0],
        [0, 9, 0, 0, 7, 0, 2, 5, 6],
        [7, 0, 0, 8, 5, 0, 0, 0, 0],
    ]

    extreme_grid = [
        [0, 4, 3, 0, 0, 0, 0, 0, 9],
        [0, 0, 0, 6, 0, 0, 0, 0, 5],
        [0, 0, 0, 0, 0, 4, 1, 0, 0],
        [9, 0, 1, 0, 5, 0, 0, 0, 0],
        [0, 0, 0, 7, 2, 6, 0, 0, 0],
        [0, 0, 8, 0, 1, 0, 0, 0, 0],
        [0, 1, 0, 0, 0, 0, 7, 2, 0],
        [7, 0, 0, 0, 0, 0, 0, 0, 0],
        [2, 0, 0, 0, 0, 5, 0, 6, 0],
    ]
    
    difficulty = argv[1] if len(argv) > 1 else "-h"

    if difficulty == 'extreme':
        grid_to_solve = extreme_grid
        print("Jemi tu solve per extreme grid")
    elif difficulty == 'hard':
        grid_to_solve = hard_grid
        print("Jemi tu solve per hard grid")
    elif difficulty == 'medium':
        grid_to_solve = medium_grid
        print("Jemi tu solve per medium grid")
    elif difficulty == 'easy': 
        grid_to_solve = easy_grid
        print("Jemi tu solve per easy grid")
    else:
        print("\nPërdorimi: ./main.py [vështirësia]")
        print("Nivelet e veshtiresise: easy, medium, hard, extreme")
        print("\n\tp.sh.: ./main.py hard\n")
        exit(0)

    board = SudokuBoard(grid_to_solve)
    print(f"Boardi fillestar eshte:\n{board}\n")
    
    solved = main(board)

    print(f"\nBoardi pas zgjidhjes eshte:\n{solved}\n")
