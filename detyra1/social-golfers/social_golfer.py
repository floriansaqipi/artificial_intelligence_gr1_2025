from itertools import combinations

def pure_dfs_social_golfers(G=8, S=4, W=9):
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

    def place(w, gi, si, used_this_week):
        if w == W:
            return True
        if gi == G:
            return place(w + 1, 0, 0, set())
        if si == S:
            return place(w, gi + 1, 0, used_this_week)

        group_members = weeks[w][gi]

        for x in range(N):
            if x in used_this_week:
                continue

            # pair-once check vs current members
            bad = False
            for m in group_members:
                if pkey(x, m) in pairs_used:
                    bad = True
                    break
            if bad:
                continue

            weeks[w][gi].append(x)
            used_this_week.add(x)

            new_pairs = []
            for m in group_members[:-1]:
                pk = pkey(x, m)
                pairs_used.add(pk)
                new_pairs.append(pk)

            if week_feasible(w, used_this_week) and place(w, gi, si + 1, used_this_week):
                return True

            for pk in new_pairs:
                pairs_used.discard(pk)
            used_this_week.remove(x)
            weeks[w][gi].pop()

        return False

    ok = place(0, 0, 0, set())
    return weeks if ok else None


if __name__ == "__main__":

    G, S, W = 8, 4, 9
    schedule = pure_dfs_social_golfers(G, S, W)
    if schedule is None:
        print("No schedule found (or search did not finish feasibly).")
    else:
        for w, week in enumerate(schedule, 1):
            print(f"Week {w}:")
            for g in week:
                print("  ", g)
