from copy import deepcopy

class BlockedNQueens:
    def __init__(self,N: int = 1, blocked_cells: list[tuple[int,int]] = None):
        self.N = N
        self.cells = [["." for _ in range(N)] for _ in range(N)] 
        for cell in blocked_cells:
            i, j = cell
            self.cells[i-1][j-1] = "X"

    def solve(self) -> BlockedNQueens:
        # implement solution here
        # make copies maybe, and return the first copy to be a solution
        root = deepcopy(self)

        pass

    def f(state: BlockedNQueens):
        return

    def g(state: BlockedNQueens):
        return

    def h(state: BlockedNQueens):
        return

    def __str__(self) -> str:
        lines = []
        for row in self.cells:
            line = []
            for cell in row:
                line.append(f"{cell}\t")
            lines.append("".join(line))
        return "\n".join(lines)
