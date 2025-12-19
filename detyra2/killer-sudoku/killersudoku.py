from copy import deepcopy

"""
    TODO:
        implement solve()
"""

class KillerSudoku:
    def solve(self) -> KillerSudoku: 
        stack = []
        initial_state = deepcopy(self)
        stack.append(initial_state)
 
        counter = 0
        while stack:
            counter += 1
            current_state = stack.pop()
            coords = current_state._next_coords()
            
            if coords is None:
                print(f"numruesi:{counter}")
                return current_state

            next_x, next_y = coords
            
            for val in range (1,10):
                next_state = deepcopy(current_state)
                try:
                    next_state._set_cell(next_x, next_y, val)
                    stack.append(next_state)
                except (CageException, ValueError) as e:
                    continue

    @staticmethod
    def fetch_board(board_dict: dict) -> KillerSudoku:
        try:
            KillerSudoku._verify_cages(board_dict)
            return KillerSudoku(board_dict["grid"], board_dict["cages"])
        except CageException as ce:
            print(f"Exception:\n{ce}")
            exit(2)
    
    @staticmethod
    def _verify_cages(board_dict: dict) -> None:
        """
            Verifies the sum of all cages (must be 405) and whether there is the same cell in 2 cages

            Raises:
                CageException: If 1 of the 2 conditions is not met
        """
        cages = board_dict["cages"]
        total_sum = sum(cage["total"] for cage in cages)
        cells = [cell for cage in cages for cell in cage["cells"]]
        
        if total_sum != 405:
            raise CageException("Kafaze jo-valide. (shuma)")
        
        if len(cells) != len(set(map(tuple, cells))):
            raise CageException("Kafaze jo-valide. (qelula duplikate)")


    def __init__(self, grid: list[list[int]]=None, cages: tuple[int, int]=None):
        self.grid = deepcopy(grid)
        self.cages = deepcopy(cages)
        self.lastRow = 1
        self.lastCol = 1

    def _set_cell(self, row: int, col: int, value: int) -> None:
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
            if value == self._get_cell(r,col):                                                   
                raise ValueError(f"Vlera {value} ekziston ne kolonën {col}.")                    
        
        # sub grid check
        big_row = (row - 1) // 3                                                                
        big_col = (col - 1) // 3                                                                
                                                                                                
        for i in range (1,4):                                                                   
            for j in range (1,4):                                                               
                if self._get_cell(big_row * 3 + i, big_col * 3 + j) == value:                    
                    raise ValueError(f"Vlera ekziston në nën-katrorin {big_row * 3 + big_col}.")

        # cage check
        """
            board: {
                grid: [
                    [11, 12, 13, 14, 15, 16, 17, 18, 19],
                    [21, 22, 23, 24, 25, 26, 27, 28, 29],
                    [31, 32, 33, 34, 35, 36, 37, 38, 39],
                    [41, 42, 43, 44, 45, 46, 47, 48, 49],
                    [51, 52, 53, 54, 55, 56, 57, 58, 59],
                    [61, 62, 63, 64, 65, 66, 67, 68, 69],
                    [71, 72, 73, 74, 75, 76, 77, 78, 79],
                    [81, 82, 83, 84, 85, 86, 87, 88, 89],
                    [91, 92, 93, 94, 95, 96, 97, 98, 99],
                ],
                cages: [
                    {total: int, cells: [[xi1,yi1] [xi2, yi2], ..., [xiN, yiN]},
                    .
                    .
                    .
                    {total: int, cells: [[xX1,yX1] [xX2, yX2], ..., [xXN, yXN]},
                ]
            }
        """
        
        for i, cage in enumerate(self.cages):
            if [row, col] not in cage["cells"]:
                continue

            # check cage total
            total = cage["total"]
            cells = cage["cells"]
            local_sum = sum(self._get_cell(cell[0],cell[1]) for cell in cells)
            
            if local_sum + value > total:
                raise CageException(f"Totali i kafazit {i}, i cili është {total}, është kaluar. Vlera aktuale: {local_sum + value}.")
            
            # check unique nums in cage
            for cell in cells:
                cell_value = self._get_cell(cell[0], cell[1])
                if cell_value == value:
                    raise CageException(f"Vlera {value} ekziston në kafaz")
                if local_sum + value > cage["total"]:
                    raise CageException(f"Vlera e kafazit është kaluar.")

                                                                                            
        self.grid[row - 1][col - 1] = value                                                     
                                                                                        
    def _get_cell(self, row: int, col: int) -> int:
        if not (1 <= row <= 9 and 1 <= col <= 9):
            raise ValueError(f"Rreshti dhe kolona duhet të jenë mes 1 dhe 9. Ata janë {row} dhe {col}.")
        return self.grid[row-1][col-1]

    def _next_coords(self) -> tuple[int, int]:
        for i in range (1, 10):
            for j in range (1, 10):
               if self._get_cell(i, j) == 0:
                    self.last_row = i
                    self.last_col = j
                    return i, j
        return None

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

class CageException(Exception):
    """Raised when a killer sudoku board has invalid cage structure."""
    pass
