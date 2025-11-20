import os

def extract_patterns(folder_path):
    output_file = "patterns.txt"
    patterns = []

    for file in os.listdir(folder_path):
        if file.endswith(".jpg"):
            # example: pattern_7-4-1-2.jpg
            name = file.split('.')[0]     # remove .jpg
            parts = name.split('_')       # split at _
            
            if len(parts) > 1:
                pattern_part = parts[1]   # 7-4-1-2
                digits = pattern_part.replace('-', '')  # remove dashes → 7412
                patterns.append(digits)

    # write to text file
    with open(output_file, "w") as f:
        for p in patterns:
            f.write(p + "\n")

    print(f"Done! Total {len(patterns)} patterns saved in {output_file}")

# ---- Run the function ----
extract_patterns(".")   # current folder
