from copy import deepcopy
from dataclass import dataclass

"""
    TODO:
        implement cage check at the end of set_cell()
        implement fetch_board()
        implement solve()
"""

class KillerSudoku:
    def fetch_board(board_dict: dict) -> KillerSudoku:
        return KillerSudoku(board_dict[grid], board_dict[cages])

   def __init__(self, grid=None: list[list[int]], cages=None: tuple[int, int]):
        self.grid = deepcopy(grid)
        self.cages = deepcopy(cages)
        self.lastRow = 1
        self.lastCol = 1

    def set_cell(self, row: int, col: int, value: int) -> void:
        # bounds and value check
        if not (1 <= row <= 9 and 1 <= col <= 9):                                               
            raise ValueError("Rreshti dhe kolona janë jasht intervalit [0-9].")                    
        if not (0 <= value <= 9):                                                               
            raise ValueError(f"Vlera {value} është jasht intervalit [0-9].")                    
                                
        # row check
        if value in self.grid[row-1]:                                                           
            raise ValueError(f"Vlera {value} eksiston në rreshtin {row}.")                       
                   
        # col check
        for r in range(1, len(self.grid)+1):                                                    
            if value == self.get_cell(r,col):                                                   
                raise ValueError(f"Vlera {value} ekziston ne kolonën {col}.")                    
        
        # sub grid check
        big_row = (row - 1) // 3                                                                
        big_col = (col - 1) // 3                                                                
                                                                                                
        for i in range (1,4):                                                                   
            for j in range (1,4):                                                               
                if self.get_cell(big_row * 3 + i, big_col * 3 + j) == value:                    
                    raise ValueError(f"Vlera ekziston në nën-katrorin {big_row * 3 + big_col}.")

        # cage check
        """
            merre vleren e cageit,
            merre ni list t kordinatave t cageit si touples,
            for touple in list
                shuma += itemi n qito coords
            if shuma != cage.shuma
                rasie ValueError(f"Kushti i limitit të shumës së elementeve të kafazit është thyer.")
        """
                                                                                            
        self.grid[row - 1][col - 1] = value                                                     
                                                                                        
    def get_cell(self, row: int, col: int) -> int:
        if not (1 <= row <= 9 and 1 <= col <= 9):
            raise ValueError(f"Rreshti dhe kolona duhet të jenë mes 1 dhe 9. Ata janë {row} dhe {col}.")
        return self.grid[row-1][col-1]

    def next_coords(self) -> tuple[int, int]:
        for i in range (1, 10):
            for j in range (1, 10):
               if self.get_cell(i, j) == 0:
                    self.last_row = i
                    self.last_col = j
                    return i, j
        return None

    def solve(self) -> KillerSudoku:
        """
            bon dfs ose diqka për me solve, bazohu n ata t kalumen
        """
        pass

    def __str__(self) -> str:
        lines = ["+-------+-------+-------+"]               
        for i, row in enumerate(self.grid):                 
            line = "| "                                     
            for j, val in enumerate(row):                   
                cell = str(val) if val != 0 else "."        
                line += cell + " "                          
                if (j + 1) % 3 == 0:                        
                    line += "| "                            
            lines.append(line)                              
            if (i + 1) % 3 == 0:                            
                lines.append("+-------+-------+-------+")   
        return "\n".join(lines)
    
    @dataclass
    class Cage:
        cells: list[tuple[int, int]]
        total: int
        
        @dataclass Cell:
            x: int
            y: int
