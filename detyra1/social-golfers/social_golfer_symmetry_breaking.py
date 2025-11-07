#!/usr/bin/env python3

import time
from math import inf
from typing import List, Optional


class SGP:

    def __init__(self, groups: int, group_size: int, weeks: int, report_every_nodes: int = 50_000,
                 max_depth_nodes: Optional[int] = None) -> None:
        self.G = groups
        self.P = group_size
        self.W = weeks
        self.N = groups * group_size
        self.max_depth_nodes = max_depth_nodes
        self.schedule: List[List[List[int]]] = [
            [[-1 for _ in range(self.P)] for _ in range(self.G)]
            for _ in range(self.W)
        ]

        self.pairs = [[False] * self.N for _ in range(self.N)]
        self.first_players: List[int] = list(range(self.G))

        self.stats = {
            "nodes": 0,
            "placements_attempted": 0,
            "backtracks": 0,
            "pair_conflicts": 0,
            "prune_week": 0,
            "prune_partner": 0,
            "prune_mrv": 0,
            "peak_depth": 0,
            "time_s": 0.0,
            "success": False,
        }
        self.report_every_nodes = report_every_nodes
        self._t0: float = 0.0

    # ------------------------------------------------------------------
    # Instrumentation helper
    # ------------------------------------------------------------------
    def _touch_node(self, depth: int, week: Optional[int] = None,
                    group: Optional[int] = None, pos: Optional[int] = None) -> None:
        self.stats["nodes"] += 1
        if depth > self.stats["peak_depth"]:
            self.stats["peak_depth"] = depth

        if self.report_every_nodes and self.stats["nodes"] % self.report_every_nodes == 0:
            elapsed = time.perf_counter() - self._t0
            rate = self.stats["nodes"] / elapsed if elapsed else 0.0
            w_str = f"{week}" if week is not None else "?"
            g_str = f"{group}" if group is not None else "?"
            p_str = f"{pos}" if pos is not None else "?"
            print(
                f"[{elapsed:6.2f}s]  nodes={self.stats['nodes']:,} "
                f"week={w_str}/{self.W} group={g_str}/{self.G} seat={p_str}/{self.P} "
                f"backs={self.stats['backtracks']:,} prunes={self.stats['prune_week']}/"
                f"{self.stats['prune_partner']}/{self.stats['prune_mrv']} "
                f"rate={rate:,.0f}/s"
            )

    # ------------------------------------------------------------------
    # Core solver logic
    # ------------------------------------------------------------------
    def _setup_first_week(self) -> None:
        for g in range(self.G):
            for p in range(self.P):
                player = g + p * self.G
                self.schedule[0][g][p] = player

        for group in self.schedule[0]:
            for i in range(self.P):
                for j in range(i + 1, self.P):
                    a, b = group[i], group[j]
                    self.pairs[a][b] = True
                    self.pairs[b][a] = True

    def solve(self) -> Optional[List[List[List[int]]]]:

        self._setup_first_week()
        self._t0 = time.perf_counter()

        success = self._solve_week(1, depth=0)

        self.stats["time_s"] = time.perf_counter() - self._t0
        self.stats["success"] = success

        if success:
            return [[list(map(lambda x: x + 1, group)) for group in week] for week in self.schedule]
        return None

    def _solve_week(self, week: int, depth: int) -> bool:
        self._touch_node(depth, week=week, group=0, pos=0)

        if self.max_depth_nodes is not None and depth > self.max_depth_nodes:
            return False

        if week == self.W:
            return True

        used_this_week = [False] * self.N
        for fp in self.first_players:
            used_this_week[fp] = True

        def assign_group(g: int, depth: int) -> bool:
            self._touch_node(depth, week=week, group=g, pos=0)

            if g == self.G:
                return self._solve_week(week + 1, depth + 1)

            fp = self.first_players[g]
            group_players = [fp] + [-1] * (self.P - 1)

            def assign_pos(pos: int, last_val: int, depth: int) -> bool:
                self._touch_node(depth, week=week, group=g, pos=pos)

                if pos == self.P:
                    self.schedule[week][g] = group_players.copy()
                    for i in range(self.P):
                        for j in range(i + 1, self.P):
                            a, b = group_players[i], group_players[j]
                            self.pairs[a][b] = True
                            self.pairs[b][a] = True

                    if assign_group(g + 1, depth + 1):
                        return True

                    for i in range(self.P):
                        for j in range(i + 1, self.P):
                            a, b = group_players[i], group_players[j]
                            self.pairs[a][b] = False
                            self.pairs[b][a] = False
                    self.stats["backtracks"] += 1
                    return False

                for candidate in range(last_val + 1, self.N):
                    if used_this_week[candidate]:
                        continue

                    valid = True
                    for i in range(pos):
                        other = group_players[i]
                        if self.pairs[candidate][other]:
                            valid = False
                            self.stats["pair_conflicts"] += 1
                            break
                    if not valid:
                        continue

                    self.stats["placements_attempted"] += 1
                    group_players[pos] = candidate
                    used_this_week[candidate] = True

                    if assign_pos(pos + 1, candidate, depth + 1):
                        return True

                    used_this_week[candidate] = False
                    group_players[pos] = -1
                    self.stats["backtracks"] += 1

                return False

            return assign_pos(1, fp, depth + 1)

        return assign_group(0, depth + 1)


def _demo() -> None:
    G, P, W = 8, 4, 6
    print(f"Demo schedule for {G}-{P}-{W}:\n")
    solver = SGP(groups=G, group_size=P, weeks=W, report_every_nodes=50_000, max_depth_nodes=inf)
    schedule = solver.solve()

    print(
        f"ok={solver.stats['success']} "
        f"time={solver.stats['time_s']:.6f}s "
        f"nodes={solver.stats['nodes']:,} "
        f"backs={solver.stats['backtracks']:,} "
        f"prunes={solver.stats['prune_week']}/"
        f"{solver.stats['prune_partner']}/{solver.stats['prune_mrv']} "
        f"placements={solver.stats['placements_attempted']:,} "
        f"pair_conflicts={solver.stats['pair_conflicts']:,} "
        f"peak_depth={solver.stats['peak_depth']}"
    )

    if schedule:
        for w, week in enumerate(schedule, start=1):
            print(f"\nWeek {w}:")
            for group in week:
                print("  ", group)
    else:
        print("No schedule found.")


if __name__ == "__main__":
    _demo()
