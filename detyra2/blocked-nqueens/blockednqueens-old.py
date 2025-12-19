from copy import deepcopy
import heapq

class BlockedNQueens:

    def __init__(self,N: int = 1, blocked_cells: list[tuple[int,int]] = None):
        self.k = 0
        self.N = N
        self.cells = [["." for _ in range(N)] for _ in range(N)] 
        for cell in blocked_cells:
            i, j = cell
            self.cells[i-1][j-1] = "X"

    def solve(self) -> bool:
        start = ()
        pq = [] # (f, g, state)
        heapq.heappush(pq, (self._h(), 0, start))

        best_g = {start: 0}

        while pq:
            f, g, state = heapq.heappop(pq)
    
            row = state.k
            if row == N:
                for i, queen_index state:
                    self.cells[i][queen_index] = "Q"
                return True

            for col in state._legal_columns():
                nxt = state.cells + (col,)
                nxt_g = nxt._g()

                if nxt_g < best_g.get(nxt, float("inf")):
                    best_g[nxt] = nxt_g
                    nxt_f = nxt._f()
                    heapq.heappush(pq, (nxt_f, nxt_g, nxt))

        return False

    def _f(self):
        return self._g() + self._h()

    def _g(self):
        return self.k

    def _h(self):
        for row in range(self.k, self.N):
            if not self._legal_columns():
                return float("inf")
        return N - k

    def _legal_columns(self):
        legal_cols = []
        row = self.k
        for col in range(self.N):
            if self.cells[row][col] == "X":
                continue
            for r, c in enumerate(self.cells):
                if c == col or abs(row-r) == abs(col-c):
                    return None
            legal_cols.append(col)
        return legal_cols

    def __str__(self) -> str:
        lines = []
        for row in self.cells:
            line = []
            for cell in row:
                line.append(f"{cell}\t")
            lines.append("".join(line))
        return "\n".join(lines)
