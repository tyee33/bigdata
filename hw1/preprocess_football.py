import glob
import os
import numpy as np
import pandas as pd

RAW_DIR = "data/raw"
OUT_DIR = "data/cleaned"
os.makedirs(OUT_DIR, exist_ok=True)

# 保留关键字段
keep_cols = [
    "Date", "Time", "HomeTeam", "AwayTeam",
    "FTHG", "FTAG", "FTR", "HTHG", "HTAG", "HTR",
    "Referee", "HS", "AS", "HST", "AST",
    "HF", "AF", "HC", "AC", "HY", "AY", "HR", "AR",
    "B365H", "B365D", "B365A"
]

frames = []

# 遍历文件并读取合并
for fp in glob.glob(os.path.join(RAW_DIR, "*.csv")):
    basename = os.path.basename(fp).replace(".csv", "")
    season, league = basename.split("_")

    try:
        df = pd.read_csv(fp, encoding="utf-8-sig")
    except Exception:
        df = pd.read_csv(fp, encoding="latin1")

    df["season"] = season
    df["league"] = league

    for c in keep_cols:
        if c not in df.columns:
            df[c] = np.nan

    df = df[keep_cols + ["season", "league"]]
    frames.append(df)

raw = pd.concat(frames, ignore_index=True)
print("原始行数：", raw.shape)

# 删除重复值
# 按照比赛日期、主队、客队、赛季、联赛进行去重
raw = raw.drop_duplicates(
    subset=["Date", "HomeTeam", "AwayTeam", "season", "league"]
)

# 数据类型转换与标准化
raw["Date"] = pd.to_datetime(raw["Date"], dayfirst=True, errors="coerce", format="mixed")
raw = raw.dropna(
    subset=["Date", "HomeTeam", "AwayTeam", "FTHG", "FTAG", "FTR"]
)

num_cols = [
    "FTHG", "FTAG", "HTHG", "HTAG",
    "HS", "AS", "HST", "AST",
    "HF", "AF", "HC", "AC",
    "HY", "AY", "HR", "AR",
    "B365H", "B365D", "B365A"
]

for c in num_cols:
    raw[c] = pd.to_numeric(raw[c], errors="coerce")

# 异常值处理
raw = raw[(raw["FTHG"].between(0, 15)) & (raw["FTAG"].between(0, 15))]

for c in ["B365H", "B365D", "B365A"]:
    raw.loc[raw[c] <= 1, c] = np.nan

# 缺失值填充与字符串清洗
for c in num_cols:
    raw[c] = raw[c].fillna(raw[c].median())

raw["Referee"] = raw["Referee"].fillna("Unknown")
raw["HomeTeam"] = raw["HomeTeam"].astype(str).str.strip()
raw["AwayTeam"] = raw["AwayTeam"].astype(str).str.strip()

# 特征工程
raw["total_goals"] = raw["FTHG"] + raw["FTAG"]
raw["goal_diff"] = raw["FTHG"] - raw["FTAG"]
raw["result"] = np.select(
    [raw["goal_diff"] > 0, raw["goal_diff"] == 0, raw["goal_diff"] < 0],
    ["HomeWin", "Draw", "AwayWin"],
    default="Unknown"
)

raw["shot_accuracy_home"] = raw["HST"] / raw["HS"].replace(0, np.nan)
raw["shot_accuracy_away"] = raw["AST"] / raw["AS"].replace(0, np.nan)
raw[["shot_accuracy_home", "shot_accuracy_away"]] = raw[
    ["shot_accuracy_home", "shot_accuracy_away"]
].fillna(0)

raw["date"] = raw["Date"].dt.strftime("%Y-%m-%d")
out = raw.drop(columns=["Date"])

out.to_csv(
    os.path.join(OUT_DIR, "football_cleaned.csv"),
    index=False,
    encoding="utf-8-sig"
)

print("清洗后行数：", out.shape)
print(out.head())