"""Create IPL analysis summary CSVs and PNG charts."""
from pathlib import Path
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import seaborn as sns

ROOT = Path(__file__).resolve().parents[1]
CLEAN = ROOT / "outputs" / "cleaned_data"
CHARTS = ROOT / "outputs" / "charts"
CHARTS.mkdir(parents=True, exist_ok=True)
sns.set_theme(style="whitegrid")

def chart(series, title, xlabel, ylabel, filename, n=10, horizontal=False):
    if series is None or series.empty:
        print("Skipped chart:", filename)
        return
    s = series.head(n)
    fig, ax = plt.subplots(figsize=(11, 6))
    if horizontal:
        s.sort_values().plot(kind="barh", ax=ax)
    else:
        s.plot(kind="bar", ax=ax)
        ax.tick_params(axis="x", rotation=40)
    ax.set_title(title, fontsize=15, weight="bold")
    ax.set_xlabel(xlabel); ax.set_ylabel(ylabel)
    fig.tight_layout()
    fig.savefig(CHARTS / filename, dpi=160)
    plt.close(fig)

def run_eda(m, d):
    if "winner" in m:
        wins = m["winner"].dropna().value_counts()
        wins.to_csv(CLEAN / "team_wins.csv", header=["wins"])
        chart(wins, "IPL Matches Won by Team", "Team", "Wins", "team_wins.png")
    batter = next((c for c in ["batter", "batsman"] if c in d), None)
    runs = next((c for c in ["batsman_runs", "batter_runs"] if c in d), None)
    if batter and runs:
        top = d.groupby(batter)[runs].sum().sort_values(ascending=False)
        top.to_csv(CLEAN / "top_batsmen.csv", header=["runs"])
        chart(top, "Top 10 Run Scorers", "Batter", "Runs", "top_batsmen.png")
    if "bowler" in d and "is_wicket" in d:
        valid = pd.to_numeric(d["is_wicket"], errors="coerce").fillna(0).eq(1)
        if "dismissal_kind" in d:
            not_credited = {"run out", "retired hurt", "retired out", "obstructing the field"}
            valid &= ~d["dismissal_kind"].astype("string").str.lower().isin(not_credited)
        topw = d.loc[valid].groupby("bowler").size().sort_values(ascending=False)
        topw.to_csv(CLEAN / "top_bowlers.csv", header=["wickets"])
        chart(topw, "Top 10 Bowler-Credited Wicket Takers", "Bowler", "Wickets", "top_bowlers.png")
    if "toss_winner" in m and "winner" in m:
        valid = m["toss_winner"].notna() & m["winner"].notna()
        rows = m.loc[valid]
        if len(rows):
            result = pd.Series({
                "Toss winner also won": int(rows["toss_winner"].eq(rows["winner"]).sum()),
                "Toss winner lost": int(rows["toss_winner"].ne(rows["winner"]).sum())
            })
            result.to_csv(CLEAN / "toss_analysis.csv", header=["matches"])
            ax = result.plot(kind="bar", figsize=(8, 5), title="Toss Winner vs Match Result")
            ax.set_xlabel(""); ax.set_ylabel("Matches"); ax.tick_params(axis="x", rotation=0)
            ax.figure.tight_layout(); ax.figure.savefig(CHARTS / "toss_analysis.png", dpi=160); plt.close(ax.figure)
    if "venue" in m:
        venues = m["venue"].dropna().value_counts()
        venues.to_csv(CLEAN / "venue_matches.csv", header=["matches"])
        chart(venues, "Matches by Venue", "Venue", "Matches", "venue_analysis.png", horizontal=True)
    mid = "id" if "id" in m else ("match_id" if "match_id" in m else None)
    if "season" in m and mid and "match_id" in d and "total_runs" in d:
        mr = d.groupby("match_id")["total_runs"].sum().rename("runs")
        sm = m[[mid, "season"]].drop_duplicates().rename(columns={mid: "match_id"})
        sr = sm.merge(mr, on="match_id", how="left").groupby("season")["runs"].sum(min_count=1)
        sr.to_csv(CLEAN / "season_runs.csv", header=["total_runs"])
        ax = sr.sort_index().plot(kind="line", marker="o", figsize=(11, 5), title="Total Runs by IPL Season")
        ax.set_xlabel("Season"); ax.set_ylabel("Runs"); ax.figure.tight_layout()
        ax.figure.savefig(CHARTS / "season_runs.png", dpi=160); plt.close(ax.figure)
    print("EDA complete. See outputs/charts and outputs/cleaned_data.")

if __name__ == "__main__":
    if not (CLEAN / "matches_cleaned.csv").exists():
        raise FileNotFoundError("Run python src/data_cleaning.py first.")
    run_eda(pd.read_csv(CLEAN / "matches_cleaned.csv"), pd.read_csv(CLEAN / "deliveries_cleaned.csv"))
