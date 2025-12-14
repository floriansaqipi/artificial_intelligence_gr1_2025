import time


def pure_dfs_social_golfers(G=8, S=4, W=9, enable_week=True, enable_partner=True, enable_mrv=True,
                            report_every_nodes=50_000):

    N = G * S
    weeks = [[[] for _ in range(G)] for _ in range(W)]
    pairs_used = set()

    stats = {
        "nodes": 0, "placements_attempted": 0, "backtracks": 0, "pair_conflicts": 0,
        "prune_week": 0, "prune_partner": 0, "prune_mrv": 0,
        "peak_depth": 0, "time_s": 0.0, "success": False
    }

    t0 = time.perf_counter()

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
        if depth > stats["peak_depth"]: stats["peak_depth"] = depth
        if report_every_nodes and stats["nodes"] % report_every_nodes == 0:
            elapsed = time.perf_counter() - t0
            rate = stats["nodes"] / elapsed if elapsed else 0
            print(f"[{elapsed:6.2f}s]  nodes={stats['nodes']:,} "
                  f"week={w}/{W} group={gi}/{G} seat={si}/{S} "
                  f"backs={stats['backtracks']:,} prunes={stats['prune_week']}/"
                  f"{stats['prune_partner']}/{stats['prune_mrv']} rate={rate:,.0f}/s")

        if w == W:
            stats["success"] = True
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
            if enable_week and not week_feasible(w, used_this_week):
                stats["prune_week"] += 1
                ok = False
            if ok and enable_mrv and not golfer_group_feasible(w, used_this_week):
                stats["prune_mrv"] += 1
                ok = False

            if ok and place(w, gi, si + 1, used_this_week, depth + 1):
                return True

            for pk in new_pairs:
                pairs_used.discard(pk)
            used_this_week.remove(x)
            weeks[w][gi].pop()
            stats["backtracks"] += 1

        return False

    ok = place(0, 0, 0, set(), 0)
    stats["time_s"] = time.perf_counter() - t0
    return (weeks if ok else None), stats


if __name__ == "__main__":

    G, S, W = 8, 4, 6
    # print("BASELINE (no pruning):")
    # schedule0, s0 = pure_dfs_social_golfers(G, S, W, enable_week=False, enable_partner=False, enable_mrv=False)
    # print(f"ok={s0['success']} time={s0['time_s']:.6f}s nodes={s0['nodes']:,} backs={s0['backtracks']:,}")
    #
    # for w, week in enumerate(schedule0, 1):
    #     print(f"Week {w}:")
    #     for g in week:
    #         print("  ", g)

    print("\nWITH PRUNING (S-k + partner@week-start + MRV):")
    schedule1, s1 = pure_dfs_social_golfers(G, S, W, enable_week=True, enable_partner=False, enable_mrv=True)
    print(f"ok={s1['success']} time={s1['time_s']:.6f}s nodes={s1['nodes']:,} backs={s1['backtracks']:,} "
          f"prunes={s1['prune_week']}/{s1['prune_partner']}/{s1['prune_mrv']}")

    for w, week in enumerate(schedule1, 1):
        print(f"Week {w}:")
        for g in week:
            print("  ", g)
