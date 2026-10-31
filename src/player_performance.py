"""Create player batting and bowling statistics."""
from pathlib import Path
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
CLEAN = ROOT / "outputs" / "cleaned_data"

def main():
    path = CLEAN / "deliveries_cleaned.csv"
    if not path.exists():
        raise FileNotFoundError("Run python src/data_cleaning.py first.")
    d = pd.read_csv(path)
    batter = next((c for c in ["batter", "batsman"] if c in d), None)
    runs = next((c for c in ["batsman_runs", "batter_runs"] if c in d), None)
    if not all([batter, runs, "bowler" in d, "is_wicket" in d]):
        raise ValueError("Required player/run/bowler/wicket columns are missing; inspect deliveries.csv.")
    d[runs] = pd.to_numeric(d[runs], errors="coerce").fillna(0)
    d["is_wicket"] = pd.to_numeric(d["is_wicket"], errors="coerce").fillna(0)
    batting = d.groupby(batter).agg(runs=(runs, "sum"), balls_faced=(batter, "size"))
    if "wide_runs" in d:
        wide = pd.to_numeric(d["wide_runs"], errors="coerce").fillna(0).gt(0)
        batting["balls_faced"] = d.assign(_legal=~wide).groupby(batter)["_legal"].sum()
    batting["strike_rate"] = (100 * batting["runs"] / batting["balls_faced"].replace(0, pd.NA)).round(2)
    batting.sort_values("runs", ascending=False).to_csv(CLEAN / "player_batting_stats.csv")
    credited = d["is_wicket"].eq(1)
    if "dismissal_kind" in d:
        excluded = {"run out", "retired hurt", "retired out", "obstructing the field"}
        credited &= ~d["dismissal_kind"].astype("string").str.lower().isin(excluded)
    bowling = d.loc[credited].groupby("bowler").size().to_frame("wickets").sort_values("wickets", ascending=False)
    bowling.to_csv(CLEAN / "player_bowling_stats.csv")
    print("Saved player_batting_stats.csv and player_bowling_stats.csv")
    print("\\nTop batters:\\n", batting.sort_values("runs", ascending=False).head(10).to_string())
    print("\\nTop bowlers:\\n", bowling.head(10).to_string())

if __name__ == "__main__":
    main()
