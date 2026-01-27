# Notes: Pattern Attempt Time Estimation (30-Second Wait)

| Dot Count | Total Patterns | Time Required (Days) |
| --------- | -------------- | -------------------- |
| 4         | 1,624          | 1 day                |
| 5         | 7,152          | 3 days               |
| 6         | 26,016         | 10 days              |
| 7         | 72,912         | 26 days              |
| 8         | 140,704        | 49 days              |
| 9         | 140,704        | 49 days              |

- This table estimates the time required to try all Android 3×3 pattern lock combinations based on the number of dots used in the pattern.

- Each pattern attempt is assumed to have a fixed waiting time of 30 seconds after an incorrect attempt.

- The calculation assumes:
  - No optimizations or shortcuts
  - No parallel attempts
  - Continuous retry availability

- Time is calculated in full days only:
  - Partial days are rounded up to the next full day.

- One full day is considered as `86,400` seconds.

- The purpose of this table is time estimation and security analysis, not practical exploitation.

### Formula Used

- `Total Time (seconds) = Total Patterns × 30`
- `Time (days) = ceil(Total Time / 86,400)`

### Interpretation

- As the dot count increases, the number of possible patterns grows rapidly.
- Higher dot-count patterns significantly increase the total time required to exhaust all possibilities.
- Even with a constant and relatively small delay (30 seconds), exhaustive attempts become a multi-week or multi-month process.
