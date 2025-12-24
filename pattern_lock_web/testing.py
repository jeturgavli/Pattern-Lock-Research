import pandas as pd
from itertools import permutations

# ====== Output CSV ======
OUTPUT_FILE = r"D:\Office Staff Daily Work\Jetur Gavli\GITHUB_JETRock\my_repo\PatternLock_Research\pattern_lock_web\all_patterns.csv"

# ====== Helper: Check if move is valid ======
# Android 3x3 grid (1–9)
# Skip over rules: if middle dot not used, can't jump
SKIP = {
    (1,3):2, (3,1):2,
    (1,7):4, (7,1):4,
    (3,9):6, (9,3):6,
    (7,9):8, (9,7):8,
    (1,9):5, (9,1):5,
    (3,7):5, (7,3):5,
    (2,8):5, (8,2):5,
    (4,6):5, (6,4):5,
}

def is_valid_move(path, next_dot):
    if not path:
        return True
    last = path[-1]
    # If skipped dot exists and not used yet, invalid
    key = (last, next_dot)
    if key in SKIP and SKIP[key] not in path:
        return False
    return True

# ====== Generate all patterns recursively ======
def generate_patterns(path, length, results):
    if len(path) == length:
        results.append(''.join(map(str, path)))
        return
    for next_dot in range(1,10):
        if next_dot not in path and is_valid_move(path, next_dot):
            generate_patterns(path + [next_dot], length, results)

all_patterns = []

# Generate patterns with length 4 to 9
for length in range(4,10):
    results = []
    generate_patterns([], length, results)
    all_patterns.extend(results)
    print(f"Generated patterns of length {length}: {len(results)}")

# ====== Prepare CSV ======
df = pd.DataFrame({
    "pattern": all_patterns,
    "dot_count": [len(p) for p in all_patterns]
})

df.to_csv(OUTPUT_FILE, index=False)
print(f"CSV file '{OUTPUT_FILE}' generated successfully with {len(df)} patterns.")

