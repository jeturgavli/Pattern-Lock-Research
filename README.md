## Android Rules 3 x 3 Grid

- Total valid patterns (length 4–9): 3,89,112

## Counts by pattern length:

| Dot Count | Total Patterns |
| --------- | ------------------------- |
| 4         | 1,624                     |
| 5         | 7,152                     |
| 6         | 26,016                    |
| 7         | 72,912                    |
| 8         | 1,40,704                  |
| 9         | 1,40,704                  |

## Android rules prohibit jumping over unused dots.

- (Example: 1→3 not allowed unless 2 already used.)
- Minimum pattern length = 4, maximum = 9.
- Total valid unique patterns = 3,89,112.

# Human-Like Android Pattern Lock Counts (4–9 Dots)

This table shows the **total number of valid Android pattern locks** based purely on **human-like rules**.

### Rules Considered:

1. **Adjacent Moves Allowed:** Moves between dots that are horizontally, vertically, or diagonally within **100px** are allowed.
2. **Center Dot Rule:** The center dot `5` can always be used in a move.
3. **Skip Rules Ignored:** Standard Android skip rules are **not considered** here.
4. **No Repetition:** Each dot can appear **only once** in a single pattern.

| Dot Count | Total Human-Like Patterns |
| --------- | ------------------------- |
| 4         | 496                       |
| 5         | 1,632                     |
| 6         | 4,032                     |
| 7         | 8,960                     |
| 8         | 15,360                    |
| 9         | 20,736                    |

> **Note:** These numbers can be exactly obtained using a DFS generation considering **only human adjacency + center dot rules**, without generating images.
