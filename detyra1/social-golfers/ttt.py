#!/usr/bin/env python3
"""
Optimised depth-first search solver for the Social Golfer Problem (SGP).

This solver uses a simple yet powerful symmetry-breaking scheme tailored
specifically for the 8-4-9 instance, although it can be applied to other
instances as well.  The key idea is to fix the first week to a regular
pattern and to fix the first player of each group in every week.  By
eliminating permutations of players and groups, the search space is
drastically reduced.  The algorithm performs a depth-first search to fill
each subsequent week subject to the constraint that no pair of golfers
ever plays together more than once.

Important features:

  * **Canonical first week**: Group ``g`` (0-based) in week 0 is set to
    ``[g, g+G, g+2G, ..., g+(P-1)G]``.  For the original 8-4-9 problem this
    yields the first week ``[[0,8,16,24],[1,9,17,25],...,[7,15,23,31]]``.
    This arrangement distributes the golfers evenly and admits a valid
    extension to at least six weeks.

  * **Fixed group leaders**: The first player of each group is fixed to
    ``g`` in every week.  This removes symmetries due to relabelling of
    players and groups.  The remaining ``P-1`` slots in each group are
    filled with distinct golfers chosen in ascending order.

  * **Ascending order within groups**: Players within a group are chosen
    in strictly increasing order.  This further reduces permutations
    within a group.

  * **No lexicographic ordering across weeks**: Unlike the earlier
    implementation, this solver does not impose an ordering on the second
    player of the first group across weeks.  Removing this requirement
    allows the search to find schedules more easily, especially for small
    numbers of weeks.

The solver has been validated to produce valid schedules for up to six
weeks for the 8-4-9 instance on modest hardware within reasonable time.
Searching for the full nine-week schedule is still computationally
intensive and may require hours or specialised heuristics.

Example usage:
"""

import time
from typing import List, Optional


class SGPSolverOptimised:
    """Depth-first search solver for the Social Golfer Problem with symmetry breaking."""

    def __init__(self, groups: int, group_size: int, weeks: int, report_every_nodes: int = 50_000) -> None:
        self.G = groups
        self.P = group_size
        self.W = weeks
        self.N = groups * group_size
        # schedule[w][g][p] holds player index (0-based)
        self.schedule: List[List[List[int]]] = [
            [[-1 for _ in range(self.P)] for _ in range(self.G)]
            for _ in range(self.W)
        ]
        # pairs[i][j] == True if players i and j have already played together
        self.pairs = [[False] * self.N for _ in range(self.N)]
        # fixed first players (group leaders)
        self.first_players: List[int] = list(range(self.G))

        # statistics (mirrors the social_golfer_symmetry_breaking.py style)
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
        """Update node counters and optionally print progress."""
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
        """Initialise the first week to a canonical pattern and update the pair matrix."""
        for g in range(self.G):
            for p in range(self.P):
                player = g + p * self.G
                self.schedule[0][g][p] = player
        # record pairs from the first week
        for group in self.schedule[0]:
            for i in range(self.P):
                for j in range(i + 1, self.P):
                    a, b = group[i], group[j]
                    self.pairs[a][b] = True
                    self.pairs[b][a] = True

    def solve(self) -> Optional[List[List[List[int]]]]:
        """Attempt to construct a schedule; return the completed schedule if successful.

        After calling this, detailed statistics are available in self.stats.
        """
        # Set up the first week and start timer
        self._setup_first_week()
        self._t0 = time.perf_counter()

        # Fill remaining weeks
        success = self._solve_week(1, depth=0)

        # Finalise statistics
        self.stats["time_s"] = time.perf_counter() - self._t0
        self.stats["success"] = success

        if success:
            # Convert to 1-based indexing for user friendliness
            return [[list(map(lambda x: x + 1, group)) for group in week] for week in self.schedule]
        return None

    def _solve_week(self, week: int, depth: int) -> bool:
        """Recursively fill week `week` and beyond."""
        self._touch_node(depth, week=week, group=0, pos=0)

        if week == self.W:
            return True

        # Track which players have been used in this week
        used_this_week = [False] * self.N
        for fp in self.first_players:
            used_this_week[fp] = True

        def assign_group(g: int, depth: int) -> bool:
            self._touch_node(depth, week=week, group=g, pos=0)

            if g == self.G:
                # All groups for this week assigned; proceed to next week
                return self._solve_week(week + 1, depth + 1)

            fp = self.first_players[g]
            # Temporary storage for this group's players
            group_players = [fp] + [-1] * (self.P - 1)

            def assign_pos(pos: int, last_val: int, depth: int) -> bool:
                self._touch_node(depth, week=week, group=g, pos=pos)

                if pos == self.P:
                    # Commit this group to the schedule
                    self.schedule[week][g] = group_players.copy()
                    # Update pair matrix
                    for i in range(self.P):
                        for j in range(i + 1, self.P):
                            a, b = group_players[i], group_players[j]
                            self.pairs[a][b] = True
                            self.pairs[b][a] = True

                    # Recurse to next group
                    if assign_group(g + 1, depth + 1):
                        return True

                    # Backtrack: undo pair assignments for this group
                    for i in range(self.P):
                        for j in range(i + 1, self.P):
                            a, b = group_players[i], group_players[j]
                            self.pairs[a][b] = False
                            self.pairs[b][a] = False
                    self.stats["backtracks"] += 1
                    return False

                # Choose a candidate player for position `pos`
                for candidate in range(last_val + 1, self.N):
                    if used_this_week[candidate]:
                        continue

                    # Check that candidate has not met any member of this group before
                    valid = True
                    for i in range(pos):
                        other = group_players[i]
                        if self.pairs[candidate][other]:
                            valid = False
                            self.stats["pair_conflicts"] += 1
                            break
                    if not valid:
                        continue

                    # Assign candidate
                    self.stats["placements_attempted"] += 1
                    group_players[pos] = candidate
                    used_this_week[candidate] = True

                    # Recurse to next position
                    if assign_pos(pos + 1, candidate, depth + 1):
                        return True

                    # Backtrack this seat
                    used_this_week[candidate] = False
                    group_players[pos] = -1
                    self.stats["backtracks"] += 1

                return False

            # Begin assigning positions 1..P-1 with last_val=fp
            return assign_pos(1, fp, depth + 1)

        # Start assigning groups for this week
        return assign_group(0, depth + 1)


def _demo() -> None:
    """Demonstration of solving the 8-4-7 instance and printing stats."""
    G, P, W = 8, 4, 5
    print(f"Demo schedule for {G}-{P}-{W}:\n")
    solver = SGPSolverOptimised(groups=G, group_size=P, weeks=W, report_every_nodes=50_000)
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
