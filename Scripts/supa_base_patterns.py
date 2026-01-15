from PIL import Image, ImageDraw, ImageFont
import os
import csv

# ------------------- FONT -------------------
try:
    font = ImageFont.truetype("arial.ttf", 18)
except:
    font = ImageFont.load_default()

# ------------------- DOT POSITIONS -------------------
positions = {
    1:(50,50), 2:(150,50), 3:(250,50),
    4:(50,150), 5:(150,150), 6:(250,150),
    7:(50,250), 8:(150,250), 9:(250,250)
}

# ------------------- NORMALIZE PATTERN -------------------
def normalize_pattern(raw):
    raw = raw.strip()

    # 1258
    if raw.isdigit():
        dots = [int(d) for d in raw]

    # 1-2-5-8 or 1,2,5,8
    else:
        raw = raw.replace(",", "-")
        dots = list(map(int, raw.split("-")))

    if (
        4 <= len(dots) <= 9 and
        all(1 <= d <= 9 for d in dots) and
        len(set(dots)) == len(dots)
    ):
        return "-".join(map(str, dots))

    return None

# ------------------- LOAD USED PATTERNS -------------------
def load_used_patterns(folder):
    used = set()

    if not os.path.exists(folder):
        return used

    for file in os.listdir(folder):
        if file.endswith(".txt"):
            with open(os.path.join(folder, file), "r", encoding="utf-8") as f:
                for line in f:
                    p = normalize_pattern(line)
                    if p:
                        used.add(p)

    return used

# ------------------- LOAD PATTERNS FROM CSV -------------------
def load_patterns_from_csv(csv_file):
    patterns = []

    with open(csv_file, newline="", encoding="utf-8-sig") as f:
        reader = csv.DictReader(f)

        print("🔎 CSV Columns:", reader.fieldnames)

        for row in reader:
            raw = None
            for key in row:
                if key.lower().strip() == "pattern":
                    raw = row[key]
                    break

            if not raw:
                continue

            p = normalize_pattern(raw)
            if p:
                patterns.append(p)

    print(f"✅ Valid patterns loaded: {len(patterns)}")
    return patterns

# ------------------- DRAW PATTERN IMAGE -------------------
def draw_pattern(pattern, output_folder):
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

        bbox = draw.textbbox((0,0), str(dot), font=font)
        w = bbox[2] - bbox[0]
        h = bbox[3] - bbox[1]
        draw.text((x-w/2, y-h/2), str(dot), font=font, fill="black")

    draw.text((img_size/2, img_size+10), pattern, anchor="mm", font=font, fill="black")

    img.save(
        os.path.join(output_folder, f"pattern_{pattern}.jpg"),
        "JPEG"
    )

# ------------------- MAIN -------------------
if __name__ == "__main__":

    csv_file = "pattern_votes_rows.csv"
    used_folder = "Used"

    output_folder = os.path.join("Output", "Real_User_Patterns")
    os.makedirs(output_folder, exist_ok=True)

    all_patterns = load_patterns_from_csv(csv_file)
    used_patterns = load_used_patterns(used_folder)

    total = len(all_patterns)
    used = 0
    generated = 0

    print(f"\n📊 Total patterns in DB: {total}")

    for pattern in all_patterns:
        if pattern in used_patterns:
            used += 1
            continue

        draw_pattern(pattern, output_folder)
        generated += 1

    print(f"✔ Already used patterns: {used}")
    print(f"🆕 New images generated: {generated}")
    print(f"⏳ Remaining unused patterns: {total - used}")
    print(f"\n📁 Images saved in → {output_folder}")
