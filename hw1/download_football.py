import os, time, requests

seasons = [f"{str(y)[2:]}{str(y+1)[2:]}" for y in range(2011, 2026)]
leagues = ["E0", "E1", "SP1", "I1", "D1", "F1"]

base = "https://www.football-data.co.uk/mmz4281/{season}/{league}.csv"
headers = {"User-Agent": "Mozilla/5.0"}
os.makedirs("data/raw", exist_ok=True)

for season in seasons:
    for code in leagues:
        url = base.format(season=season, league=code)
        fn = f"data/raw/{season}_{code}.csv"
        if os.path.exists(fn):
            continue
        r = requests.get(url, headers=headers, timeout=30)
        if r.status_code == 200 and len(r.content) > 1000:
            with open(fn, "wb") as f:
                f.write(r.content)
            print("OK", fn)
        else:
            print("FAIL", url, r.status_code)
        time.sleep(0.5)