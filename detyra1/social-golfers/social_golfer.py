def pure_dfs_social_golfers(G=8, S=4, W=9):
    stats = {
        "nodes": 0,  # recursive calls
        "placements_attempted": 0,  # trying a golfer in a seat
        "pair_conflicts": 0,  # rejected due to pair already met
        "backtracks": 0,  # undo after exploring child
        "prunes_week_feasible": 0,  # S-k forward-check prunes
        "peak_depth": 0,
    }

    N = G * S
    weeks = [[[] for _ in range(G)] for _ in range(W)]
    pairs_used = set()

    def pkey(a, b):
        if a > b: a, b = b, a
        return a * N + b

    def week_feasible(w, used_this_week):
        for gi in range(G):
            group = weeks[w][gi]
            k = len(group)
            if k == S:
                continue
            need = S - k
            legal = 0
            for x in range(N):
                if x in used_this_week:
                    continue
                ok = True
                for m in group:
                    if pkey(x, m) in pairs_used:
                        ok = False
                        break
                if ok:
                    legal += 1
                    if legal >= need:
                        break
            if legal < need:
                return False
        return True

    def partner_budget_feasible(used_this_week):
        unassigned = [x for x in range(N) if x not in used_this_week]
        U = len(unassigned)
        if U == 0:
            return True
        if U < S:
            return False
        for i, x in enumerate(unassigned):
            partners = 0
            for j, y in enumerate(unassigned):
                if y == x:
                    continue
                if pkey(x, y) not in pairs_used:
                    partners += 1
                    if partners >= S - 1:
                        break
            if partners < S - 1:
                return False
        return True

    def golfer_group_feasible(w, used_this_week):
        unassigned = [x for x in range(N) if x not in used_this_week]
        if not unassigned:
            return True

        for x in unassigned:
            can_join_any = False
            for gi in range(G):
                group = weeks[w][gi]
                if len(group) >= S:
                    continue

                ok = True
                for m in group:
                    if pkey(x, m) in pairs_used:
                        ok = False
                        break
                if ok:
                    can_join_any = True
                    break
            if not can_join_any:
                return False
        return True

    def place(w, gi, si, used_this_week, depth):
        stats["nodes"] += 1
        if depth > stats["peak_depth"]:
            stats["peak_depth"] = depth

        if w == W:
            return True
        if gi == G:
            return place(w + 1, 0, 0, set(), depth + 1)
        if si == S:
            return place(w, gi + 1, 0, used_this_week, depth + 1)

        group_members = weeks[w][gi]

        for x in range(N):
            if x in used_this_week:
                continue

            # pair-once check vs current members
            bad = False
            for m in group_members:
                if pkey(x, m) in pairs_used:
                    stats["pair_conflicts"] += 1
                    bad = True
                    break
            if bad:
                continue

            stats["placements_attempted"] += 1
            weeks[w][gi].append(x)
            used_this_week.add(x)

            new_pairs = []
            for m in group_members[:-1]:
                pk = pkey(x, m)
                pairs_used.add(pk)
                new_pairs.append(pk)

            ok = True
            if not week_feasible(w, used_this_week):
                stats["prunes_week_feasible"] += 1
                ok = False

            if (ok and place(w, gi, si + 1, used_this_week, depth + 1)
                    and partner_budget_feasible(used_this_week)
                    and golfer_group_feasible(w, used_this_week)):
                return True

            for pk in new_pairs:
                pairs_used.discard(pk)
            used_this_week.remove(x)
            weeks[w][gi].pop()
            stats["backtracks"] += 1

        return False

    ok = place(0, 0, 0, set(), 0)
    return weeks if ok else None


if __name__ == "__main__":

    G, S, W = 8, 4, 6
    schedule = pure_dfs_social_golfers(G, S, W)
    if schedule is None:
        print("No schedule found (or search did not finish feasibly).")
    else:
        for w, week in enumerate(schedule, 1):
            print(f"Week {w}:")
            for g in week:
                print("  ", g)
