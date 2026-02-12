import os
import json

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
JSON_DIR = os.path.join(BASE_DIR, "JSON_PATTERNS")
USED_DIR = os.path.join(BASE_DIR, "Used")


def load_json_database():
    dot_db = {d: set() for d in range(4, 10)}

    for dot in range(4, 10):
        folder = os.path.join(JSON_DIR, f"{dot}_DOT")

        if not os.path.exists(folder):
            continue

        for file in os.listdir(folder):
            if file.endswith(".json"):
                try:
                    with open(os.path.join(folder, file), "r") as f:
                        data = json.load(f)

                        # Always using patterns[] list
                        patterns = data.get("patterns", [])

                        for p in patterns:
                            p = p.strip()
                            if p.isdigit() and len(p) == dot:
                                dot_db[dot].add(p)
                except:
                    pass

    return dot_db


def load_used_patterns():
    used = {d: set() for d in range(4, 10)}

    for file in os.listdir(USED_DIR):
        if not file.endswith(".txt"):
            continue

        with open(os.path.join(USED_DIR, file), "r") as f:
            for line in f:
                p = line.strip()
                if p.isdigit() and 4 <= len(p) <= 9:
                    used[len(p)].add(p)

    return used


def main():
    print("\n------------ DOT-WISE PATTERN COUNTER ------------\n")

    json_db = load_json_database()
    used = load_used_patterns()

    grand_total = 0
    grand_used = 0

    for dot in range(4, 10):
        total = len(json_db[dot])
        used_in_db = len(json_db[dot].intersection(used[dot]))
        remaining = total - used_in_db

        grand_total += total
        grand_used += used_in_db

        print(f"{dot} DOT:")
        print(f"   Total Patterns (JSON DB): {total}")
        print(f"   Used Patterns (Matched) : {used_in_db}")
        print(f"   Remaining Patterns      : {remaining}")
        print("--------------------------------------------------")

    grand_remaining = grand_total - grand_used

    print("\n============== GRAND TOTAL ==============")
    print(f"Total Patterns (All Dots) : {grand_total}")
    print(f"Used Patterns (Matched)   : {grand_used}")
    print(f"Remaining Patterns        : {grand_remaining}")
    print("=========================================\n")



if __name__ == "__main__":
    main()
