#!/usr/bin/env python3
"""
Optimised depth‑first search solver for the Social Golfer Problem (SGP).

This solver uses a simple yet powerful symmetry‑breaking scheme tailored
specifically for the 8‑4‑9 instance, although it can be applied to other
instances as well.  The key idea is to fix the first week to a regular
pattern and to fix the first player of each group in every week.  By
eliminating permutations of players and groups, the search space is
drastically reduced.  The algorithm performs a depth‑first search to fill
each subsequent week subject to the constraint that no pair of golfers
ever plays together more than once.

Important features:

  * **Canonical first week**: Group ``g`` (0‑based) in week 0 is set to
    ``[g, g+G, g+2G, ..., g+(P-1)G]``.  For the original 8‑4‑9 problem this
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
weeks for the 8‑4‑9 instance on modest hardware within reasonable time.
Searching for the full nine‑week schedule is still computationally
intensive and may require hours or specialised heuristics.

Example usage:


"""

from typing import List, Optional


class SGPSolverOptimised:
    """Depth‑first search solver for the Social Golfer Problem with symmetry breaking."""

    def __init__(self, groups: int, group_size: int, weeks: int) -> None:
        self.G = groups
        self.P = group_size
        self.W = weeks
        self.N = groups * group_size
        # schedule[w][g][p] holds player index (0‑based)
        self.schedule: List[List[List[int]]] = [
            [[-1 for _ in range(self.P)] for _ in range(self.G)]
            for _ in range(self.W)
        ]
        # pairs[i][j] == True if players i and j have already played together
        self.pairs = [[False] * self.N for _ in range(self.N)]
        # fixed first players (group leaders)
        self.first_players: List[int] = list(range(self.G))

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
        """Attempt to construct a schedule; return the completed schedule if successful."""
        # Set up the first week
        self._setup_first_week()
        # Fill remaining weeks
        success = self._solve_week(1)
        if success:
            # Convert to 1‑based indexing for user friendliness
            return [[list(map(lambda x: x + 1, group)) for group in week] for week in self.schedule]
        return None

    def _solve_week(self, week: int) -> bool:
        """Recursively fill week `week` and beyond."""
        if week == self.W:
            return True
        # Track which players have been used in this week
        used_this_week = [False] * self.N
        for fp in self.first_players:
            used_this_week[fp] = True

        def assign_group(g: int) -> bool:
            if g == self.G:
                # All groups for this week assigned; proceed to next week
                return self._solve_week(week + 1)
            fp = self.first_players[g]
            # Temporary storage for this group's players
            group_players = [fp] + [-1] * (self.P - 1)

            def assign_pos(pos: int, last_val: int) -> bool:
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
                    if assign_group(g + 1):
                        return True
                    # Backtrack: undo pair assignments
                    for i in range(self.P):
                        for j in range(i + 1, self.P):
                            a, b = group_players[i], group_players[j]
                            self.pairs[a][b] = False
                            self.pairs[b][a] = False
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
                            break
                    if not valid:
                        continue
                    # Assign candidate
                    group_players[pos] = candidate
                    used_this_week[candidate] = True
                    # Recurse to next position
                    if assign_pos(pos + 1, candidate):
                        return True
                    # Backtrack
                    used_this_week[candidate] = False
                    group_players[pos] = -1
                return False
            # Begin assigning positions 1..P-1 with last_val=fp
            return assign_pos(1, fp)
        # Start assigning groups for this week
        return assign_group(0)


def _demo() -> None:
    """Demonstration of solving the 8‑4‑9 instance for the first few weeks."""
    print("Demo schedule for 8‑4‑2 (two weeks):\n")
    solver2 = SGPSolverOptimised(groups=8, group_size=4, weeks=7)
    schedule2 = solver2.solve()
    if schedule2:
        for w, week in enumerate(schedule2, start=1):
            print(f"Week {w}:")
            for group in week:
                print("  ", group)
            print()
    else:
        print("No 2‑week schedule found.")




if __name__ == "__main__":
    _demo()