import sys
from collections import defaultdict

current_key = None
current_count = 0
stats = defaultdict(int)

for line in sys.stdin:
    line = line.strip()
    try:
        key, count = line.split("\t")
        count = int(count)
    except ValueError:
        continue

    if current_key == key:
        current_count += count
    else:
        if current_key:
            stats[current_key] = current_count
        current_key = key
        current_count = count

# 最后一个 key
if current_key:
    stats[current_key] = current_count

# 打印汇总结果
for k, v in stats.items():
    print(f"{k}\t{v}")