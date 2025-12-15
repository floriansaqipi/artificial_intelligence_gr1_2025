#!/usr/bin/env python3
from __future__ import annotations
from typing import Dict, List

from pysat.formula import CNF
from pysat.solvers import Glucose3


GUESTS = 100
TABLES = 10
CAPACITY = 10


def var_id(g: int, t: int, T: int) -> int:
    return (g - 1) * T + t


def decode(model: List[int]) -> Dict[int, int]:
    pos = set(l for l in model if l > 0)
    gt: Dict[int, int] = {}
    for g in range(1, GUESTS + 1):
        for t in range(1, TABLES + 1):
            if var_id(g, t, TABLES) in pos:
                gt[g] = t
                break
    return gt


def main() -> None:
    cnf = CNF(from_file="seating.cnf")

    with Glucose3(bootstrap_with=cnf.clauses) as s:
        if not s.solve():
            print("UNSAT")
            return
        model = s.get_model()

    gt = decode(model)

    table_to_guests = {t: [] for t in range(1, TABLES + 1)}
    for g, t in gt.items():
        table_to_guests[t].append(g)

    print("SAT\n")
    for t in range(1, TABLES + 1):
        guests_here = sorted(table_to_guests[t])
        males = sum(1 for g in guests_here if g % 2 == 0)
        females = CAPACITY - males
        print(f"Table {t:2d}: {guests_here} | M={males}, F={females}, diff={abs(males-females)}")


if __name__ == "__main__":
    main()
