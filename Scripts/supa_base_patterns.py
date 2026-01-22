from PIL import Image, ImageDraw, ImageFont
import os
import csv

# =================== PATH FIX (IMPORTANT) ===================
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
BASE_DIR = os.path.dirname(SCRIPT_DIR)

CSV_FILE = os.path.join(SCRIPT_DIR, "pattern_votes_rows.csv")
USED_FOLDER = os.path.join(BASE_DIR, "Used")
OUTPUT_FOLDER = os.path.join(BASE_DIR, "Output", "Real_User_Patterns")

os.makedirs(OUTPUT_FOLDER, exist_ok=True)

# =================== FONT ===================
try:
    font = ImageFont.truetype("arial.ttf", 18)
except:
    font = ImageFont.load_default()

# =================== DOT POSITIONS ===================
positions = {
    1:(50,50), 2:(150,50), 3:(250,50),
    4:(50,150), 5:(150,150), 6:(250,150),
    7:(50,250), 8:(150,250), 9:(250,250)
}

# =================== NORMALIZE PATTERN ===================
def normalize_pattern(raw):
    if not raw:
        return None

    raw = raw.strip()

    if raw.isdigit():                     # 1258
        dots = [int(d) for d in raw]
    else:                                 # 1-2-5-8 , 1,2,5,8
        raw = raw.replace(",", "-")
        parts = raw.split("-")
        if not all(p.isdigit() for p in parts):
            return None
        dots = list(map(int, parts))

    if (
        4 <= len(dots) <= 9 and
        all(1 <= d <= 9 for d in dots) and
        len(set(dots)) == len(dots)
    ):
        return "-".join(map(str, dots))

    return None

# =================== LOAD USED PATTERNS ===================
def load_used_patterns(folder):
    used = set()

    if not os.path.exists(folder):
        print("❌ Used folder not found:", folder)
        return used

    for file in os.listdir(folder):
        if file.endswith(".txt"):
            file_path = os.path.join(folder, file)
            with open(file_path, "r", encoding="utf-8") as f:
                for line in f:
                    p = normalize_pattern(line)
                    if p:
                        used.add(p)

    return used

# =================== LOAD CSV PATTERNS ===================
def load_patterns_from_csv(csv_file):
    patterns = []

    with open(csv_file, newline="", encoding="utf-8-sig") as f:
        reader = csv.DictReader(f)

        for row in reader:
            raw = None
            for key in row:
                if key.lower().strip() == "pattern":
                    raw = row[key]
                    break

            p = normalize_pattern(raw)
            if p:
                patterns.append(p)

    return patterns

# =================== DRAW IMAGE ===================
def draw_pattern(pattern):
    radius = 20
    img_size = 300
    pattern_list = list(map(int, pattern.split("-")))

    img = Image.new("RGB", (img_size, img_size+40), "white")
    draw = ImageDraw.Draw(img)

    for i in range(len(pattern_list)-1):
        x1, y1 = positions[pattern_list[i]]
        x2, y2 = positions[pattern_list[i+1]]
        draw.line((x1, y1, x2, y2), width=4, fill="black")

    for dot, (x, y) in positions.items():
        fill = "orange" if dot in pattern_list else "lightgrey"
        draw.ellipse(
            (x-radius, y-radius, x+radius, y+radius),
            fill=fill,
            outline="black",
            width=2
        )

        w, h = draw.textbbox((0,0), str(dot), font=font)[2:]
        draw.text((x-w/2, y-h/2), str(dot), font=font, fill="black")

    draw.text((img_size/2, img_size+10), pattern, anchor="mm", font=font, fill="black")

    img.save(os.path.join(OUTPUT_FOLDER, f"pattern_{pattern}.jpg"), "JPEG")

# =================== MAIN ===================
if __name__ == "__main__":

    all_patterns = load_patterns_from_csv(CSV_FILE)
    used_patterns = load_used_patterns(USED_FOLDER)

    print("📂 Used folder:", USED_FOLDER)
    print("📊 Used patterns loaded:", len(used_patterns))
    print("📊 Total CSV patterns:", len(all_patterns))

    used = 0
    generated = 0

    for pattern in all_patterns:
        if pattern in used_patterns:
            used += 1
            continue

        draw_pattern(pattern)
        generated += 1

    print("\n✔ Already used patterns skipped:", used)
    print("🆕 New images generated:", generated)
    print("📁 Output →", OUTPUT_FOLDER)
