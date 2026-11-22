import sys

# 读取 CSV 的每一行
for line in sys.stdin:
    line = line.strip()
    if not line or line.startswith("HomeTeam,"): # 跳过表头
        continue
    cols = line.split(",")
    try:
        league = cols[25] 
        result = cols[4] 
        print(f"{league}_{result}\t1")
    except IndexError:
        continue