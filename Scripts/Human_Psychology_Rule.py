from PIL import Image, ImageDraw, ImageFont
import os

# ------------------- Load Font Early -------------------
try:
    font = ImageFont.truetype("arial.ttf", 18)
except:
    font = ImageFont.load_default()

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

# ------------------- Human Psychology Rule -------------------
def is_human_move_ok(a, b):
    ax, ay = positions[a]
    bx, by = positions[b]
    dx = abs(ax - bx)
    dy = abs(ay - by)

    # same dot invalid
    if a == b:
        return False

    # Center 5 is always allowed (common human move)
    if b == 5:
        return True

    # Adjacent horizontally / vertically / diagonally (≤ 100 px)
    if dx <= 100 and dy <= 100:
        return True

    # far jumps are not allowed
    return False


# ------------------- DFS generator -------------------
def dfs(visited, cur, length, patterns):
    if len(visited) == length:
        patterns.append(visited[:])
        return

    for next_dot in range(1,10):
        if next_dot not in visited:

            # -------- Human Psychology Rule --------
            if not is_human_move_ok(cur, next_dot):
                continue

            # -------- Android Skip Rule --------
            if skip[cur][next_dot] == 0 or skip[cur][next_dot] in visited:
                dfs(visited+[next_dot], next_dot, length, patterns)

# ------------------- Load USED patterns -------------------
def load_used_patterns(used_folder):
    used = set()
    if not os.path.exists(used_folder):
        return used
        
    for file in os.listdir(used_folder):
        if file.endswith(".txt"):
            with open(os.path.join(used_folder, file), "r") as f:
                for line in f:
                    line = line.strip()
                    if line != "":
                        used.add(line)
    return used

# ------------------- Draw Pattern -------------------
def draw_pattern(pattern, output_folder):
    radius = 20
    img_size = 300
    img = Image.new("RGB", (img_size, img_size+40), "white")
    draw = ImageDraw.Draw(img)

    # draw pattern lines
    for i in range(len(pattern)-1):
        x1, y1 = positions[pattern[i]]
        x2, y2 = positions[pattern[i+1]]
        draw.line((x1, y1, x2, y2), width=4, fill="black")

    # draw dots
    for dot, (x, y) in positions.items():
        fill_color = "orange" if dot in pattern else "lightgrey"
        draw.ellipse(
            (x-radius, y-radius, x+radius, y+radius),
            fill=fill_color, outline="black", width=2
        )

        bbox = draw.textbbox((0,0), str(dot), font=font)
        w = bbox[2] - bbox[0]
        h = bbox[3] - bbox[1]
        draw.text((x - w/2, y - h/2), str(dot), font=font, fill="black")

    # pattern text
    pattern_text = ",".join(map(str, pattern))
    draw.text((img_size/2, img_size+10), pattern_text, anchor="mm", font=font, fill="black")

    file_name = f"pattern_{'-'.join(map(str, pattern))}.jpg"
    img.save(os.path.join(output_folder, file_name), "JPEG")


# ------------------- Main -------------------
if __name__ == "__main__":
    while True:
        try:
            dot_count = int(input("Enter DOT count (4-9): "))
            if 4 <= dot_count <= 9:
                break
        except:
            pass
        print("Invalid input. Enter 4-9.")

    while True:
        try:
            start_dot = int(input("Enter start dot (1-9): "))
            if 1 <= start_dot <= 9:
                break
        except:
            pass
        print("Invalid input. Enter 1-9.")

    # Load USED patterns
    used_folder = os.path.join("..", "Used")
    used_patterns = load_used_patterns(used_folder)

    used_key_set = {"-".join(list(p)) for p in used_patterns}

    patterns = []
    dfs([start_dot], start_dot, dot_count, patterns)

    print(f"Total HUMAN-LIKE valid patterns starting with {start_dot}: {len(patterns)}")

    main_folder = os.path.join("..","Output", f"patterns_{dot_count}_dot_HUMAN")
    sub_folder = os.path.join(main_folder, f"patterns_start_{start_dot}")
    os.makedirs(sub_folder, exist_ok=True)

    saved = 0
    skipped = 0

    for pattern in patterns:
        key = "-".join(map(str, pattern))
        if key in used_key_set:
            skipped += 1
            continue

        draw_pattern(pattern, sub_folder)
        saved += 1

    print(f"\n✔ Saved (unique + human-like) patterns: {saved}")
    print(f"✘ Skipped (used): {skipped}")
    print(f"\nImages saved in → {sub_folder}")
