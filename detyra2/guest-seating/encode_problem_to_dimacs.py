#!/usr/bin/env python3
from __future__ import annotations
from dataclasses import dataclass, field
from typing import List, Tuple

from pysat.formula import CNF
from pysat.card import CardEnc

Pair = Tuple[int, int]
Group = Tuple[int, ...]


@dataclass
class SeatingProblem:
    guests: int = 100
    tables: int = 10
    capacity: int = 10
    gender_diff: int = 3
    not_together: List[Pair] = field(default_factory=list)
    together_groups: List[Group] = field(default_factory=list)
    card_encoding: int = 1


def var_id(g: int, t: int, T: int) -> int:
    return (g - 1) * T + t


def add_atmost(cnf: CNF, lits: List[int], k: int, top_id: int, encoding: int) -> int:
    if k >= len(lits):
        return top_id
    enc = CardEnc.atmost(lits=lits, bound=k, top_id=top_id, encoding=encoding)
    cnf.extend(enc.clauses)
    return max(top_id, enc.nv)


def build_cnf(p: SeatingProblem) -> CNF:
    if p.guests != p.tables * p.capacity:
        raise ValueError("This encoder assumes guests == tables*capacity (100 == 10*10).")

    for grp in p.together_groups:
        if len(grp) > p.capacity:
            raise ValueError(f"Together-group {grp} too large for capacity {p.capacity}.")

    cnf = CNF()
    G, T = p.guests, p.tables
    top_id = G * T  # main vars are 1..1000

    # Exactly one table per guest
    for g in range(1, G + 1):
        lits = [var_id(g, t, T) for t in range(1, T + 1)]
        cnf.append(lits)  # at least one
        top_id = add_atmost(cnf, lits, 1, top_id, p.card_encoding)

    # Capacity per table: AtMost 10 (=> exactly 10 because total seats = guests)
    for t in range(1, T + 1):
        lits = [var_id(g, t, T) for g in range(1, G + 1)]
        top_id = add_atmost(cnf, lits, p.capacity, top_id, p.card_encoding)

    # Not-together pairs
    for a, b in p.not_together:
        for t in range(1, T + 1):
            cnf.append([-var_id(a, t, T), -var_id(b, t, T)])

    # Together groups (leader equivalence)
    for grp in p.together_groups:
        if len(grp) < 2:
            continue
        leader = grp[0]
        for k in grp[1:]:
            for t in range(1, T + 1):
                cnf.append([-var_id(leader, t, T),  var_id(k, t, T)])
                cnf.append([-var_id(k, t, T),       var_id(leader, t, T)])

    # Gender balance per table: AtMost upper for males AND females
    upper = (p.capacity + p.gender_diff) // 2  # 6
    males = [g for g in range(1, G + 1) if g % 2 == 0]
    females = [g for g in range(1, G + 1) if g % 2 == 1]

    for t in range(1, T + 1):
        top_id = add_atmost(cnf, [var_id(g, t, T) for g in males], upper, top_id, p.card_encoding)
        top_id = add_atmost(cnf, [var_id(g, t, T) for g in females], upper, top_id, p.card_encoding)

    return cnf


def main() -> None:
    # Fill these with YOUR constraints
    not_together = [
        # (1, 5), (2, 9),
    ]
    together_groups = [
        # (10, 11, 12),
    ]

    p = SeatingProblem(
        guests=100, tables=10, capacity=10, gender_diff=3,
        not_together=not_together,
        together_groups=together_groups,
        card_encoding=1,
    )

    cnf = build_cnf(p)
    cnf.to_file("seating.cnf")
    print(f"Wrote seating.cnf  (vars={cnf.nv}, clauses={len(cnf.clauses)})")


if __name__ == "__main__":
    main()
