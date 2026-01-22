import os

# ------------------- Android skip rules -------------------
skip = [[0]*10 for _ in range(10)]
skip[1][3] = skip[3][1] = 2
skip[1][7] = skip[7][1] = 4
skip[3][9] = skip[9][3] = 6
skip[7][9] = skip[9][7] = 8
skip[1][9] = skip[9][1] = 5
skip[3][7] = skip[7][3] = 5
skip[4][6] = skip[6][4] = 5
skip[2][8] = skip[8][2] = 5

# ------------------- Dot positions -------------------
positions = {
    1:(50,50), 2:(150,50), 3:(250,50),
    4:(50,150), 5:(150,150), 6:(250,150),
    7:(50,250), 8:(150,250), 9:(250,250)
}

# ------------------- Human psychology rule -------------------
def is_human_move_ok(a, b):
    if a == b:
        return False

    ax, ay = positions[a]
    bx, by = positions[b]

    dx = abs(ax - bx)
    dy = abs(ay - by)

    if b == 5:
        return True

    if dx <= 100 and dy <= 100:
        return True

    return False

# ------------------- DFS generator -------------------
def dfs(visited, cur, length, results):
    if len(visited) == length:
        results.append("".join(map(str, visited)))
        return

    for nxt in range(1, 10):
        if nxt not in visited:

            if not is_human_move_ok(cur, nxt):
                continue

            if skip[cur][nxt] == 0 or skip[cur][nxt] in visited:
                dfs(visited + [nxt], nxt, length, results)

# ------------------- MAIN -------------------
if __name__ == "__main__":

    BASE_DIR = "TEXT_PATTERNS"
    os.makedirs(BASE_DIR, exist_ok=True)

    print("==========================================")
    print(" ANDROID HUMAN PATTERN DATABASE GENERATOR ")
    print("==========================================\n")

    for dot_count in range(4, 10):

        dot_folder = os.path.join(BASE_DIR, f"{dot_count}_DOT")
        os.makedirs(dot_folder, exist_ok=True)

        print(f"▶ Generating {dot_count}_DOT patterns")

        for start_dot in range(1, 10):
            patterns = []
            dfs([start_dot], start_dot, dot_count, patterns)

            file_path = os.path.join(
                dot_folder,
                f"PATTERN_START_{start_dot}.txt"
            )

            with open(file_path, "w") as f:
                for p in patterns:
                    f.write(p + "\n")

            print(
                f"   START {start_dot} → "
                f"{len(patterns)} patterns saved"
            )

        print("------------------------------------------")

    print("\n✔ ALL DOT PATTERN FILES GENERATED SUCCESSFULLY")
