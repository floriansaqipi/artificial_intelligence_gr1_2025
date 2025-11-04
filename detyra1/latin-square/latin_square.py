from anytree import Node, RenderTree

import copy
from utils import is_valid, find_empty_cell, print_latin_square

def _dls(grid, n, depth_limit, current_depth):
    
    if current_depth == depth_limit:
        if find_empty_cell(grid, n) == (None, None):
            return ("GOAL", [copy.deepcopy(grid)])  
        else:
            return ("CUTOFF", []) 

    (r, c) = find_empty_cell(grid, n)
    
    if r is None:
        return ("GOAL", [copy.deepcopy(grid)])

    cutoff_occurred = False
    all_solutions_found = []
    
    for val in range(1, n + 1):
        if is_valid(grid, n, r, c, val):
            grid[r][c] = val
            
            (status, results) = _dls(grid, n, depth_limit, current_depth + 1)
            
            if status == "GOAL":
                all_solutions_found.extend(results)
                if len(results) > 1:
                    print(f"Gjetëm {len(results)} zgjidhje të reja:")
                else:
                    print(f"Gjetëm {len(results)} zgjidhje të re:")
                for i, result in enumerate(results):
                    print(f"Zgjidhja {i + len(all_solutions_found)}:")
                    print_latin_square(result)
                    print("\n")
                 
            if status == "CUTOFF":
                cutoff_occurred = True
            
            grid[r][c] = None

    if all_solutions_found:
        return ("GOAL", all_solutions_found)
    elif cutoff_occurred:
        return ("CUTOFF", [])
    else:
        return ("FAILURE", [])

def iddfs_solve_latin_square(n):
    start_grid = [[None for _ in range(n)] for _ in range(n)]
    
    total_cells = n * n
    
    all_solutions = []
    
    for limit in range(total_cells + 1):
        print(f"Duke provuar në thellsinë {limit}...")

        grid_copy = copy.deepcopy(start_grid)
        
        (status, results) = _dls(grid_copy, n, limit, 0)
        
        if status == "GOAL":
            if limit == total_cells:
                print(f"\nGjetëm {len(results)} zgjidhje në thellsinë {limit}!")
                all_solutions.extend(results)
        
        if status == "CUTOFF":
            print(f"Kërkimi u ndalua. Po eksplorojmë më thell...", end='\n--\n')
        
        if status == "FAILURE":
            print("Dega dështoi.")
    
    if not all_solutions:
        print(f"\nAsnjë zgjidhje nuk u gjet. Kërkuam deri në thellsinë {total_cells}.")
        return None
    else:
        return all_solutions