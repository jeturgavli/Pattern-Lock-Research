from PIL import Image, ImageDraw, ImageFont
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

# ------------------- Dot positions (3x3 grid) -------------------
positions = {
    1:(50,50), 2:(150,50), 3:(250,50),
    4:(50,150), 5:(150,150), 6:(250,150),
    7:(50,250), 8:(150,250), 9:(250,250)
}

# ------------------- DFS for valid patterns -------------------
def dfs(visited, cur, length, patterns):
    if len(visited) == length:
        patterns.append(visited[:])
        return
    for next_dot in range(1,10):
        if next_dot not in visited:
            if skip[cur][next_dot]==0 or skip[cur][next_dot] in visited:
                dfs(visited+[next_dot], next_dot, length, patterns)

# ------------------- Draw pattern image -------------------
def draw_pattern(pattern, output_folder):
    radius = 20
    img_size = 300
    img = Image.new("RGB", (img_size, img_size+40), "white")
    draw = ImageDraw.Draw(img)

    # Draw connecting lines
    for i in range(len(pattern)-1):
        x1, y1 = positions[pattern[i]]
        x2, y2 = positions[pattern[i+1]]
        draw.line((x1, y1, x2, y2), fill="blue", width=4)

    # Draw numbered balls
    for dot, (x, y) in positions.items():
        if dot in pattern:
            fill_color = "orange"
            text_color = "white"
        else:
            fill_color = "lightgrey"
            text_color = "black"
        draw.ellipse((x-radius, y-radius, x+radius, y+radius), fill=fill_color, outline="black", width=2)
        
        bbox = draw.textbbox((0,0), str(dot), font=font)
        w = bbox[2] - bbox[0]
        h = bbox[3] - bbox[1]
        draw.text((x - w/2, y - h/2), str(dot), fill=text_color, font=font)

    # Pattern number text
    pattern_text = ",".join(map(str, pattern))
    draw.text((img_size/2, img_size+10), pattern_text, fill="black", anchor="mm", font=font)

    # Save file
    file_name = f"pattern_{'-'.join(map(str, pattern))}.jpg"
    file_path = os.path.join(output_folder, file_name)
    img.save(file_path, "JPEG")

# ------------------- Main -------------------
if __name__ == "__main__":
    # 1️⃣ User input for DOT count
    while True:
        try:
            dot_count = int(input("Enter DOT count (4-9): "))
            if 4 <= dot_count <= 9:
                break
            else:
                print("Invalid input. Choose between 4 and 9.")
        except ValueError:
            print("Invalid input. Enter a number 4-9.")

    # 2️⃣ User input for start dot
    while True:
        try:
            start_dot = int(input("Enter start dot (1-9): "))
            if 1 <= start_dot <= 9:
                break
            else:
                print("Invalid input. Choose between 1 and 9.")
        except ValueError:
            print("Invalid input. Enter a number 1-9.")

    # 3️⃣ Generate patterns starting from selected start dot
    patterns = []
    dfs([start_dot], start_dot, dot_count, patterns)
    print(f"Total valid {dot_count}-dot patterns starting with {start_dot}: {len(patterns)}")

    # 4️⃣ Font setup
    try:
        font = ImageFont.truetype("arial.ttf", 18)
    except:
        font = ImageFont.load_default()

    # 5️⃣ Setup output folder
    main_folder = os.path.join(".","Output", f"patterns_{dot_count}_dot")
    sub_folder = os.path.join(main_folder, f"patterns_start_{start_dot}")
    os.makedirs(sub_folder, exist_ok=True)

    # 6️⃣ Generate images
    for idx, pattern in enumerate(patterns, start=1):
        draw_pattern(pattern, sub_folder)
        if idx % 100 == 0:
            print(f"{idx} patterns saved...")

    print(f"✅ All {len(patterns)} pattern images saved in '{sub_folder}' folder.")
