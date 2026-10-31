"""Clean common IPL match and ball-by-ball CSV schemas."""
from pathlib import Path
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "dataset"
OUT = ROOT / "outputs" / "cleaned_data"

def load_datasets():
    mp, dp = DATA / "matches.csv", DATA / "deliveries.csv"
    if not mp.exists() or not dp.exists():
        raise FileNotFoundError("Put matches.csv and deliveries.csv inside the dataset/ folder.")
    m, d = pd.read_csv(mp), pd.read_csv(dp)
    m.columns = [str(c).strip().lower().replace(" ", "_") for c in m.columns]
    d.columns = [str(c).strip().lower().replace(" ", "_") for c in d.columns]
    return m, d

def rename_first(df, mapping):
    renames = {}
    lookup = {c.lower(): c for c in df.columns}
    for canonical, options in mapping.items():
        for option in options:
            if option.lower() in lookup:
                renames[lookup[option.lower()]] = canonical
                break
    return df.rename(columns=renames)

def clean_datasets(matches, deliveries):
    m, d = matches.copy(), deliveries.copy()
    m = rename_first(m, {
        "id": ["id", "match_id"], "season": ["season", "year"], "date": ["date"],
        "team1": ["team1", "team_1"], "team2": ["team2", "team_2"],
        "toss_winner": ["toss_winner"], "winner": ["winner", "match_winner"],
        "venue": ["venue", "stadium"], "result": ["result"],
    })
    d = rename_first(d, {
        "match_id": ["match_id", "id"], "inning": ["inning", "innings"],
        "over": ["over", "overs"], "ball": ["ball", "delivery"],
        "batter": ["batter", "batsman", "striker"], "bowler": ["bowler"],
        "batsman_runs": ["batsman_runs", "batter_runs", "runs_off_bat"],
        "extra_runs": ["extra_runs", "extras"], "total_runs": ["total_runs", "runs_total"],
        "is_wicket": ["is_wicket", "wicket"], "dismissal_kind": ["dismissal_kind", "kind"],
        "player_dismissed": ["player_dismissed", "dismissed_player"],
        "batting_team": ["batting_team"], "bowling_team": ["bowling_team"],
        "wide_runs": ["wide_runs"],
    })
    m, d = m.drop_duplicates().copy(), d.drop_duplicates().copy()
    if "date" in m:
        m["date"] = pd.to_datetime(m["date"], errors="coerce")
    for col in ["id", "season"]:
        if col in m:
            m[col] = pd.to_numeric(m[col], errors="coerce")
    for col in ["match_id", "inning", "over", "ball", "batsman_runs", "extra_runs", "total_runs", "is_wicket", "wide_runs"]:
        if col in d:
            d[col] = pd.to_numeric(d[col], errors="coerce")
    for col in ["team1", "team2", "toss_winner", "winner", "venue"]:
        if col in m:
            m[col] = m[col].astype("string").str.strip().replace({"": pd.NA, "nan": pd.NA, "None": pd.NA})
    if "season" not in m and "date" in m:
        m["season"] = m["date"].dt.year
    return m, d

def save_cleaned(matches, deliveries):
    OUT.mkdir(parents=True, exist_ok=True)
    matches.to_csv(OUT / "matches_cleaned.csv", index=False)
    deliveries.to_csv(OUT / "deliveries_cleaned.csv", index=False)
    print("Saved cleaned datasets to", OUT)

if __name__ == "__main__":
    matches, deliveries = load_datasets()
    matches, deliveries = clean_datasets(matches, deliveries)
    save_cleaned(matches, deliveries)
    print(f"Rows: {len(matches):,} matches; {len(deliveries):,} deliveries")
