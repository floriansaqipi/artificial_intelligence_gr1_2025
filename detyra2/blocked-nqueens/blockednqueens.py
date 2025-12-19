from copy import deepcopy
import heapq

class BlockedNQueens:

    def __init__(
            self,
            blocked_cells: list[tuple[int,int]] = None,
            N: int = 1,
            state: tuple = () 
            ):
        self.N = N
        self.state = state
        self.blocked_cells = blocked_cells

    def solve(self) -> bool:
        root_state = deepcopy(self)
        pqueue = []
        heapq.heappush(pqueue, (root_state.f(), root_state.g(), root_state))

        best_g = {root_state: 0}
        return_flag = False
        
        while pqueue:
            f, g, curr_state = heapq.heappop(pqueue)
            
            if g == self.N:
                return_flag = True
                break

            for col in curr_state.legal_columns():
                nxt = BlockedNQueens(
                        blocked_cells=self.blocked_cells,
                        N=self.N,
                        state=curr_state.state + (col,)
                        )

                if nxt.g() < best_g.get(nxt, float("inf")):
                    best_g[nxt] = nxt.g()
                    heapq.heappush(pqueue, (nxt.f(), nxt.g(), nxt)) 
        
        self.state = curr_state.state
        return return_flag

    def f(self): # funksioni vlersus
        return self.g() + self.h()

    def g(self): # cost funksioni
        return len(self.state)

    def h(self): # funksioni heuristik 
                 # - numri i rreshtave t'bllokum
        for row in range(len(self.state), self.N):
            if not self.legal_columns():
                return float("inf")
        return self.N - len(self.state)

    def legal_columns(self): # 
        legal_cols = []
        row = len(self.state)
        
        for col in range(self.N):
            if (row, col) in self.blocked_cells:
                continue

            ok = True
            for r, c in enumerate(self.state):
                if col == c or abs(row-r) == abs(col-c):
                    ok = False
                    break
            if ok:
                legal_cols.append(col)

        return legal_cols

    def __str__(self) -> str:
        grid = [[".\t" for _ in range(self.N)] for _ in range(self.N)]
        
        for row, col in enumerate(self.state):
            grid[row][col] = "Q\t"
        
        for row, col in self.blocked_cells:
            grid[row][col] = "X\t"
       
        lines = []
        for row in grid:
            lines.append("".join(row))
        
        return "\n".join(lines)

    def __lt__(self, other) -> bool:
        return (self.state < other.state)
