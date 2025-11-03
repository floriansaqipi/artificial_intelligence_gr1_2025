from itertools import combinations

def pure_dfs_social_golfers(G=8, S=4, W=9):

    N = G * S
    golfers = list(range(N))


    weeks = [[[] for _ in range(G)] for _ in range(W)]


    pairs_used = set()


    def pkey(a, b):
        if a > b: a, b = b, a
        return a * N + b

    def place(w, gi, si, used_this_week):

        if w == W:
            return True
        if gi == G:
            return place(w + 1, 0, 0, set())

        if si == S:
            return place(w, gi + 1, 0, used_this_week)


        for x in range(N):
            if x in used_this_week:
                continue

            group_members = weeks[w][gi]
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
            for m in group_members:
                pk = pkey(x, m)
                pairs_used.add(pk)
                new_pairs.append(pk)


            if place(w, gi, si + 1, used_this_week):
                return True

            for pk in new_pairs:
                pairs_used.remove(pk)
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
