import streamlit as st
import pandas as pd
import plotly.express as px
from pathlib import Path

# ============================================================
# IPL PULSE — ANIMATED IPL DATA ANALYSIS DASHBOARD
# Save this file as dashboard_app.py in your project root.
# Expected CSVs: dataset/matches.csv and dataset/deliveries.csv
# ============================================================

st.set_page_config(
    page_title="IPL PULSE | Cricket Analytics",
    page_icon="🏏",
    layout="wide",
    initial_sidebar_state="expanded",
)

BASE_DIR = Path(__file__).resolve().parent
DATASET_DIR = BASE_DIR / "dataset"
MATCHES_FILE = DATASET_DIR / "matches.csv"
DELIVERIES_FILE = DATASET_DIR / "deliveries.csv"

# --------------------------- CSS -----------------------------
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;500;600;700;800&family=Inter:wght@300;400;500;600;700;800&display=swap');

:root { --bg:#070817; --purple:#a855f7; --cyan:#00f5ff; --pink:#ff3cac; }
html, body, [data-testid="stAppViewContainer"] {
    background:#070817; color:#f5f7ff; font-family:'Inter',sans-serif;
}
[data-testid="stAppViewContainer"] {
    background:
      radial-gradient(ellipse at 12% 8%, rgba(87,32,155,.28), transparent 40%),
      radial-gradient(ellipse at 88% 28%, rgba(0,145,180,.16), transparent 38%),
      linear-gradient(135deg,#070817,#0b1025,#100a24);
    background-size:200% 200%;
    animation:bgMove 16s ease infinite;
}
@keyframes bgMove { 0%,100%{background-position:0% 50%} 50%{background-position:100% 50%} }
[data-testid="stHeader"] { background:transparent; }
[data-testid="stSidebar"] {
    background:linear-gradient(180deg,#100d29,#080b1b);
    border-right:1px solid rgba(0,245,255,.28);
}
[data-testid="stSidebar"] * { color:#f0f4ff; }
.block-container { padding-top:1.4rem; padding-bottom:3rem; max-width:1500px; }
.hero {
    position:relative; overflow:hidden; padding:32px 30px; border-radius:24px;
    margin-bottom:22px;
    background:linear-gradient(115deg,rgba(116,37,255,.23),rgba(0,245,255,.08),rgba(255,60,172,.16));
    background-size:300% 300%; border:1px solid rgba(0,245,255,.35);
    box-shadow:0 0 25px rgba(0,245,255,.08),inset 0 0 35px rgba(168,85,247,.07);
    animation:heroGradient 9s ease infinite;
}
@keyframes heroGradient { 0%,100%{background-position:0% 50%} 50%{background-position:100% 50%} }
.hero-title {
    font-family:'Orbitron',sans-serif; font-size:clamp(29px,4.5vw,52px);
    font-weight:800; letter-spacing:3px; line-height:1.3; margin:0;
    background:linear-gradient(90deg,#fff,#00f5ff,#c084fc,#fff);
    background-size:250% auto; color:transparent; -webkit-background-clip:text;
    background-clip:text; animation:titleShine 5s linear infinite;
}
@keyframes titleShine { to{background-position:250% center} }
.hero-subtitle { color:#b6c4e7; font-size:13px; margin-top:12px; letter-spacing:1.4px; }
.hero-badge {
    display:inline-block; margin-top:15px; padding:7px 13px; border-radius:30px;
    background:rgba(0,245,255,.08); border:1px solid rgba(0,245,255,.45);
    color:#00f5ff; font-size:11px; letter-spacing:1.6px;
    animation:badgePulse 2s ease-in-out infinite;
}
@keyframes badgePulse { 0%,100%{box-shadow:0 0 4px rgba(0,245,255,.1)} 50%{box-shadow:0 0 18px rgba(0,245,255,.35)} }
.floating-ball { font-size:78px; text-align:center; filter:drop-shadow(0 0 16px rgba(0,245,255,.45)); animation:ballFloat 3s ease-in-out infinite; }
@keyframes ballFloat { 0%,100%{transform:translateY(0) rotate(-8deg)} 50%{transform:translateY(-14px) rotate(12deg)} }
.section-title { font-family:'Orbitron',sans-serif; font-size:19px; color:#fff; letter-spacing:1px; margin:20px 0 14px; }
.section-title span { color:#00f5ff; }
.kpi-card {
    position:relative; overflow:hidden; padding:20px 18px; min-height:135px; border-radius:18px;
    background:linear-gradient(140deg,rgba(30,35,73,.92),rgba(13,17,40,.95));
    border:1px solid rgba(124,132,255,.30);
    transition:transform .3s ease,box-shadow .3s ease,border-color .3s ease;
    animation:cardEntrance .7s ease both;
}
.kpi-card:hover { transform:translateY(-6px) scale(1.015); border-color:#00f5ff; box-shadow:0 0 22px rgba(0,245,255,.18),0 12px 30px rgba(0,0,0,.25); }
.kpi-card:after { content:""; position:absolute; top:-80%; left:-100%; width:70%; height:250%; background:linear-gradient(90deg,transparent,rgba(255,255,255,.07),transparent); transform:rotate(25deg); transition:left .7s ease; }
.kpi-card:hover:after { left:140%; }
@keyframes cardEntrance { from{opacity:0;transform:translateY(16px)} to{opacity:1;transform:translateY(0)} }
.kpi-icon { font-size:25px; margin-bottom:8px; }
.kpi-label { color:#a9b8df; font-size:11px; letter-spacing:1.3px; text-transform:uppercase; }
.kpi-value { font-family:'Orbitron',sans-serif; font-size:clamp(22px,2.2vw,32px); font-weight:700; color:#fff; margin-top:8px; overflow-wrap:anywhere; }
.kpi-note { font-size:11px; color:#00ffa3; margin-top:7px; }
[data-testid="stPlotlyChart"] { border-radius:17px; border:1px solid rgba(124,132,255,.18); padding:4px; background:rgba(15,19,43,.48); transition:border-color .3s,box-shadow .3s; }
[data-testid="stPlotlyChart"]:hover { border-color:rgba(0,245,255,.5); box-shadow:0 0 20px rgba(0,245,255,.07); }
.stButton button, .stDownloadButton button {
    border-radius:11px; border:1px solid rgba(0,245,255,.5);
    background:linear-gradient(100deg,#6328db,#087ea4); color:#fff; font-weight:700;
    transition:all .3s ease;
}
.stButton button:hover, .stDownloadButton button:hover { border-color:#00f5ff; box-shadow:0 0 18px rgba(0,245,255,.4); transform:translateY(-2px); }
[data-baseweb="select"] > div { background:#151a35; border-color:rgba(124,132,255,.4); border-radius:10px; }
[data-testid="stDataFrame"] { border:1px solid rgba(0,245,255,.2); border-radius:12px; }
.stadium-container {
    position:relative; height:270px; overflow:hidden; border-radius:22px; margin:18px 0 26px;
    isolation:isolate; background:radial-gradient(ellipse at 50% 110%,rgba(0,255,170,.32),transparent 55%),linear-gradient(180deg,#030817 0%,#10133b 45%,#073c42 100%);
    border:1px solid rgba(0,245,255,.42); box-shadow:0 0 25px rgba(0,245,255,.1),inset 0 0 35px rgba(124,58,237,.18);
}
.stadium-sky { position:absolute; inset:0; background:radial-gradient(circle at 15% 20%,rgba(255,255,255,.8) 1px,transparent 2px),radial-gradient(circle at 75% 15%,rgba(255,255,255,.6) 1px,transparent 2px),radial-gradient(circle at 55% 30%,rgba(255,255,255,.7) 1px,transparent 2px); animation:stars 4s ease-in-out infinite alternate; }
@keyframes stars { from{opacity:.3} to{opacity:1} }
.floodlight { position:absolute; top:22px; width:7px; height:72px; border-radius:8px; background:#fff; box-shadow:0 0 8px #fff,0 0 25px #00f5ff,0 0 60px rgba(0,245,255,.75); animation:lightPulse 2.5s ease-in-out infinite alternate; }
.floodlight.left { left:12%; } .floodlight.right { right:12%; animation-delay:1.2s; }
@keyframes lightPulse { from{opacity:.65;filter:brightness(.8)} to{opacity:1;filter:brightness(1.5)} }
.light-beam { position:absolute; top:60px; width:210px; height:220px; background:linear-gradient(180deg,rgba(0,245,255,.12),transparent); clip-path:polygon(35% 0,65% 0,100% 100%,0 100%); filter:blur(15px); animation:beamGlow 3s ease-in-out infinite alternate; }
.light-beam.left { left:0; } .light-beam.right { right:0; }
@keyframes beamGlow { from{opacity:.3} to{opacity:.85} }
.stadium-crowd { position:absolute; top:105px; left:5%; width:90%; height:65px; border-radius:50% 50% 0 0; background:repeating-linear-gradient(90deg,#171c46 0,#171c46 4px,#252d61 4px,#252d61 8px); border-top:3px solid rgba(0,245,255,.45); }
.stadium-field { position:absolute; left:-10%; bottom:-155px; width:120%; height:320px; border-radius:50% 50% 0 0; background:repeating-linear-gradient(90deg,#087a48 0,#087a48 60px,#096b40 60px,#096b40 120px); border-top:4px solid rgba(0,255,163,.7); transform:perspective(400px) rotateX(8deg); }
.stadium-pitch { position:absolute; bottom:15px; left:42%; width:16%; height:80px; background:linear-gradient(90deg,#bda67d,#ead7a3,#bda67d); clip-path:polygon(30% 0,70% 0,100% 100%,0 100%); opacity:.85; }
.stadium-ball { position:absolute; z-index:3; top:85px; left:50%; font-size:34px; filter:drop-shadow(0 0 15px #ff3cac); animation:stadiumBall 4s ease-in-out infinite; }
@keyframes stadiumBall { 0%,100%{transform:translate(-50%,0) rotate(0)} 25%{transform:translate(calc(-50% + 30px),-20px) rotate(90deg)} 50%{transform:translate(-50%,-38px) rotate(180deg)} 75%{transform:translate(calc(-50% - 30px),-16px) rotate(270deg)} }
.stadium-title { position:absolute; z-index:5; top:25px; left:0; width:100%; text-align:center; font-family:'Orbitron',sans-serif; font-size:clamp(18px,3vw,30px); font-weight:800; letter-spacing:3px; color:#fff; text-shadow:0 0 10px #00f5ff,0 0 25px rgba(0,245,255,.7); }
.stadium-subtitle { position:absolute; z-index:5; top:65px; left:0; width:100%; text-align:center; font-size:10px; letter-spacing:3px; color:#9efcff; }
.footer { margin-top:38px; padding:22px; text-align:center; border-top:1px solid rgba(124,132,255,.2); color:#8e9cc2; font-size:12px; letter-spacing:1px; }
.footer span { color:#00f5ff; }
@media(max-width:768px) { .hero{padding:24px 18px}.floating-ball{font-size:52px}.stadium-container{height:235px}.stadium-crowd{top:95px}.kpi-card{padding:15px;min-height:120px}.section-title{font-size:16px} }
</style>
""", unsafe_allow_html=True)

# ------------------------ DATA LOADING -----------------------
@st.cache_data
def load_data():
    if not MATCHES_FILE.exists():
        raise FileNotFoundError(f"Missing file: {MATCHES_FILE}")
    if not DELIVERIES_FILE.exists():
        raise FileNotFoundError(f"Missing file: {DELIVERIES_FILE}")

    matches = pd.read_csv(MATCHES_FILE)
    deliveries = pd.read_csv(DELIVERIES_FILE)

    matches.columns = [str(c).strip().lower().replace(" ", "_") for c in matches.columns]
    deliveries.columns = [str(c).strip().lower().replace(" ", "_") for c in deliveries.columns]

    if "match_id" in matches.columns and "id" not in matches.columns:
        matches = matches.rename(columns={"match_id": "id"})
    if "season_id" in matches.columns and "season" not in matches.columns:
        matches = matches.rename(columns={"season_id": "season"})
    if "batsman" in deliveries.columns and "batter" not in deliveries.columns:
        deliveries = deliveries.rename(columns={"batsman": "batter"})
    if "batsman_runs" in deliveries.columns and "batter_runs" not in deliveries.columns:
        deliveries = deliveries.rename(columns={"batsman_runs": "batter_runs"})
    if "inning" in deliveries.columns and "innings" not in deliveries.columns:
        deliveries = deliveries.rename(columns={"inning": "innings"})

    if "match_id" not in deliveries.columns:
        if "id" in deliveries.columns:
            deliveries = deliveries.rename(columns={"id": "match_id"})
        else:
            raise ValueError("deliveries.csv needs a match_id column.")

    if "season" not in matches.columns:
        if "date" in matches.columns:
            matches["season"] = pd.to_datetime(matches["date"], errors="coerce").dt.year.astype("Int64").astype(str)
        else:
            matches["season"] = "Unknown"
    matches["season"] = matches["season"].astype(str)

    return matches, deliveries

try:
    matches, deliveries = load_data()
except Exception as exc:
    st.error(f"Could not load the IPL dataset: {exc}")
    st.info("Check that dataset/matches.csv and dataset/deliveries.csv exist in your project.")
    st.stop()

# Normalize important numeric columns
for col in ["total_runs", "batter_runs", "is_wicket"]:
    if col in deliveries.columns:
        deliveries[col] = pd.to_numeric(deliveries[col], errors="coerce").fillna(0)

# ----------------------- SIDEBAR NAV -------------------------
st.sidebar.markdown("""
<div style="text-align:center;padding:12px 0 8px">
  <div style="font-size:42px">🏏</div>
  <div style="font-family:Orbitron;font-size:22px;color:#00f5ff">IPL PULSE</div>
  <div style="color:#9ba9d2;font-size:10px;letter-spacing:2px">CRICKET INTELLIGENCE</div>
</div>
""", unsafe_allow_html=True)
st.sidebar.markdown("---")
st.sidebar.markdown("### 🧭 Dashboard Navigation")

page = st.sidebar.radio(
    "Go to section",
    [
        "Home",
        "Performance Overview",
        "Team Intelligence",
        "Run & Scoring Analysis",
        "Player Performance Lab",
        "Top Wicket Takers",
        "Match Explorer",
    ],
    label_visibility="collapsed",
)

st.sidebar.markdown("---")
st.sidebar.markdown("### 🎛️ Filters")

season_options = sorted(matches["season"].dropna().astype(str).unique().tolist())
selected_seasons = st.sidebar.multiselect("📅 Seasons", season_options, default=season_options)

team_cols = [c for c in ["team1", "team2", "winner"] if c in matches.columns]
team_options = sorted({
    str(team)
    for col in team_cols
    for team in matches[col].dropna().unique()
})
selected_teams = st.sidebar.multiselect("🏆 Teams", team_options, default=team_options)

if st.sidebar.button("🔄 Refresh dashboard", use_container_width=True):
    st.cache_data.clear()
    st.rerun()

st.sidebar.markdown("""
<div style="font-size:11px;color:#8997bd;line-height:2;margin-top:18px">
⚡ Interactive Analytics<br>📊 Match Statistics<br>🎯 Player Performance<br>💎 Neon Interface
</div>
""", unsafe_allow_html=True)

# ------------------------- FILTER DATA -----------------------
fm = matches[matches["season"].astype(str).isin(selected_seasons)].copy()
if team_cols:
    if selected_teams:
        team_mask = pd.Series(False, index=fm.index)
        for col in team_cols:
            team_mask |= fm[col].astype(str).isin(selected_teams)
        fm = fm[team_mask]
    else:
        fm = fm.iloc[0:0]
else:
    if not selected_teams:
        fm = fm.iloc[0:0]

match_ids = set(fm["id"].dropna()) if "id" in fm.columns else set()
fd = deliveries[deliveries["match_id"].isin(match_ids)].copy()

runs_total = int(fd["total_runs"].sum()) if "total_runs" in fd.columns else 0
wickets_total = int(fd["is_wicket"].sum()) if "is_wicket" in fd.columns else (
    int(fd["dismissal_kind"].notna().sum()) if "dismissal_kind" in fd.columns else 0
)
team_count = len({str(t) for c in ["team1", "team2"] if c in fm.columns for t in fm[c].dropna().unique()})

# Wicket-taker calculation: prefer bowler + dismissal_kind, exclude dismissals
# generally not credited to the bowler when that field is available.
def get_top_wicket_takers(delivery_frame):
    if "bowler" not in delivery_frame.columns:
        return pd.DataFrame(columns=["Bowler", "Wickets"])

    temp = delivery_frame.copy()
    if "dismissal_kind" in temp.columns:
        credited_dismissals = {
            "bowled", "caught", "caught and bowled", "lbw",
            "stumped", "hit wicket", "hit the ball twice",
            "handled the ball", "obstructing the field"
        }
        # Older datasets may include run-out and retired-hurt rows.
        temp["dismissal_kind"] = temp["dismissal_kind"].astype(str).str.lower().str.strip()
        temp = temp[temp["dismissal_kind"].isin(credited_dismissals)]
        grouped = temp.groupby("bowler").size().reset_index(name="Wickets")
    elif "is_wicket" in temp.columns:
        # Fallback when dismissal_kind is unavailable; may include run-outs.
        temp = temp[temp["is_wicket"] > 0]
        grouped = temp.groupby("bowler")["is_wicket"].sum().reset_index(name="Wickets")
    else:
        return pd.DataFrame(columns=["Bowler", "Wickets"])

    grouped = grouped.rename(columns={"bowler": "Bowler"})
    return grouped.sort_values("Wickets", ascending=False)

top_wickets = get_top_wicket_takers(fd)

# Shared chart styling
COLORS = ["#00f5ff", "#a855f7", "#ff3cac", "#00ffa3", "#facc15", "#60a5fa", "#fb923c"]
def style_chart(fig, height=390):
    fig.update_layout(
        template="plotly_dark",
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(family="Inter", color="#dbeafe", size=12),
        margin=dict(l=25, r=20, t=65, b=35),
        title_font=dict(family="Orbitron", size=15, color="#ffffff"),
        hoverlabel=dict(bgcolor="#151a35", bordercolor="#00f5ff", font_color="#ffffff"),
        height=height,
        transition=dict(duration=650, easing="cubic-in-out"),
    )
    return fig

def section_heading(icon, first, second):
    st.markdown(
        f'<div class="section-title">{icon} <span>{first}</span>{second}</div>',
        unsafe_allow_html=True,
    )

# -------------------------- PAGE: HOME -----------------------
if page == "Home":
    # Keep the large welcome hero and stadium animation on Home only.
    hero_left, hero_right = st.columns([4, 1])
    with hero_left:
        st.markdown("""
        <div class="hero">
          <div class="hero-title">IPL PULSE</div>
          <div class="hero-subtitle">THE NEXT GENERATION OF CRICKET ANALYTICS</div>
          <div class="hero-badge">✦ DATA • INSIGHTS • PERFORMANCE ✦</div>
        </div>
        """, unsafe_allow_html=True)
    with hero_right:
        st.markdown('<div style="padding-top:25px"><div class="floating-ball">🏏</div></div>', unsafe_allow_html=True)

    st.markdown("""
    <div class="stadium-container">
      <div class="stadium-sky"></div>
      <div class="light-beam left"></div><div class="light-beam right"></div>
      <div class="floodlight left"></div><div class="floodlight right"></div>
      <div class="stadium-title">IPL NIGHT ARENA</div>
      <div class="stadium-subtitle">CRICKET • PASSION • PERFORMANCE</div>
      <div class="stadium-crowd"></div>
      <div class="stadium-field"></div>
      <div class="stadium-pitch"></div>
      <div class="stadium-ball">🏏</div>
    </div>
    """, unsafe_allow_html=True)

    section_heading("🏠", "HOME", " DASHBOARD")

    st.markdown("""
    <div class="hero">
      <div style="font-family:Orbitron,sans-serif;font-size:clamp(22px,3vw,34px);
                  font-weight:800;color:#ffffff;letter-spacing:1.5px;">
        WELCOME TO THE IPL PULSE ARENA
      </div>
      <div class="hero-subtitle">
        YOUR CENTRAL HUB FOR IPL MATCHES, TEAM INSIGHTS, RUNS AND PLAYER PERFORMANCE
      </div>
      <div class="hero-badge">✦ SELECT A SECTION FROM THE SIDEBAR TO EXPLORE ✦</div>
    </div>
    """, unsafe_allow_html=True)

    home_kpis = [
        ("🏟️", "MATCHES ANALYZED", f"{len(fm):,}", "Based on current filters"),
        ("🔥", "TOTAL RUNS", f"{runs_total:,}", "Runs in selected matches"),
        ("🎯", "TOTAL WICKETS", f"{wickets_total:,}", "Recorded wicket events"),
        ("🏆", "TEAMS", f"{team_count:,}", "Teams in selection"),
    ]
    home_cols = st.columns(4)
    for col, (icon, label, value, note) in zip(home_cols, home_kpis):
        with col:
            st.markdown(f"""<div class="kpi-card"><div class="kpi-icon">{icon}</div>
            <div class="kpi-label">{label}</div><div class="kpi-value">{value}</div>
            <div class="kpi-note">✦ {note}</div></div>""", unsafe_allow_html=True)

    section_heading("🧭", "EXPLORE", " YOUR ANALYTICS")
    home_cards = [
        ("📊", "Team Intelligence", "Compare team wins and review team performance."),
        ("🔥", "Run & Scoring Analysis", "Explore high-scoring matches and leading batters."),
        ("🎯", "Player Performance Lab", "Inspect individual player runs, fours, sixes and strike rate."),
        ("🏆", "Top Wicket Takers", "Rank bowlers by credited wickets."),
        ("🔎", "Match Explorer", "Filter and download match records."),
        ("⚡", "Performance Overview", "See key metrics and season trends."),
    ]
    card_cols = st.columns(3)
    for index, (icon, title, description) in enumerate(home_cards):
        with card_cols[index % 3]:
            st.markdown(f"""
            <div class="kpi-card" style="margin-bottom:16px;min-height:155px;">
              <div class="kpi-icon">{icon}</div>
              <div style="font-family:Orbitron,sans-serif;color:#00f5ff;
                          font-size:14px;font-weight:700;margin-bottom:10px;">{title}</div>
              <div style="font-size:12px;line-height:1.7;color:#a9b8df;">{description}</div>
            </div>
            """, unsafe_allow_html=True)

    st.caption("Use the sidebar navigation to open each section. Statistics update when you change the season or team filters.")

# --------------------- PAGE: OVERVIEW ------------------------
elif page == "Performance Overview":
    section_heading("⚡", "PERFORMANCE", " OVERVIEW")
    kpis = [
        ("🏟️", "MATCHES ANALYZED", f"{len(fm):,}", "Selected matches"),
        ("🔥", "TOTAL RUNS", f"{runs_total:,}", "Runs in selected matches"),
        ("🎯", "TOTAL WICKETS", f"{wickets_total:,}", "Recorded wicket events"),
        ("🏆", "TEAMS", f"{team_count:,}", "Teams in selection"),
    ]
    cols = st.columns(4)
    for col, (icon, label, value, note) in zip(cols, kpis):
        with col:
            st.markdown(f"""<div class="kpi-card"><div class="kpi-icon">{icon}</div>
            <div class="kpi-label">{label}</div><div class="kpi-value">{value}</div>
            <div class="kpi-note">✦ {note}</div></div>""", unsafe_allow_html=True)

    c1, c2 = st.columns(2)
    with c1:
        if "winner" in fm.columns and not fm.empty:
            wins = fm["winner"].dropna().value_counts().rename_axis("Team").reset_index(name="Wins")
            fig = px.bar(wins.sort_values("Wins"), x="Wins", y="Team", orientation="h",
                         title="🏆 Match Wins by Team", color="Wins",
                         color_continuous_scale=["#312e81", "#a855f7", "#00f5ff"], text="Wins")
            fig.update_layout(coloraxis_showscale=False, yaxis_title="", xaxis_title="Wins")
            fig.update_traces(textposition="outside")
            st.plotly_chart(style_chart(fig), use_container_width=True)
        else:
            st.info("No winner information is available for the selected filters.")
    with c2:
        if not fm.empty:
            season_counts = fm.groupby("season").size().reset_index(name="Matches")
            season_counts["season"] = season_counts["season"].astype(str)
            fig = px.area(season_counts, x="season", y="Matches", markers=True,
                          title="📈 Matches Across Seasons", color_discrete_sequence=["#00f5ff"])
            fig.update_traces(line=dict(width=3), fillcolor="rgba(0,245,255,.12)", marker=dict(size=8))
            st.plotly_chart(style_chart(fig), use_container_width=True)
        else:
            st.info("Choose at least one season and team.")

# --------------------- PAGE: TEAM INTELLIGENCE ---------------
elif page == "Team Intelligence":
    section_heading("📊", "TEAM", " INTELLIGENCE")
    if "winner" in fm.columns and not fm.empty:
        wins = fm["winner"].dropna().value_counts().rename_axis("Team").reset_index(name="Wins")
        c1, c2 = st.columns(2)
        with c1:
            fig = px.bar(wins.sort_values("Wins"), x="Wins", y="Team", orientation="h",
                         title="🏆 Most Match Wins", color="Wins",
                         color_continuous_scale=["#312e81", "#a855f7", "#00f5ff"], text="Wins")
            fig.update_layout(coloraxis_showscale=False, yaxis_title="")
            fig.update_traces(textposition="outside")
            st.plotly_chart(style_chart(fig), use_container_width=True)
        with c2:
            fig = px.pie(wins, names="Team", values="Wins", hole=.58,
                         title="🥇 Share of Recorded Wins", color_discrete_sequence=COLORS)
            fig.update_traces(textposition="inside", textinfo="percent+label",
                              marker=dict(line=dict(color="#070817", width=2)))
            st.plotly_chart(style_chart(fig), use_container_width=True)
        st.dataframe(wins, use_container_width=True, hide_index=True)
    else:
        st.info("No team winner data for this selection.")

# --------------------- PAGE: RUN & SCORING -------------------
elif page == "Run & Scoring Analysis":
    section_heading("🔥", "RUN & SCORING", " ANALYSIS")
    c1, c2 = st.columns(2)
    with c1:
        if "match_id" in fd.columns and "total_runs" in fd.columns and not fd.empty:
            by_match = fd.groupby("match_id")["total_runs"].sum().nlargest(15).sort_values().reset_index(name="Runs")
            by_match["Match ID"] = by_match["match_id"].astype(str)
            fig = px.bar(by_match, x="Runs", y="Match ID", orientation="h",
                         title="⚡ Highest-Scoring Matches (Top 15)", color="Runs",
                         color_continuous_scale=["#312e81", "#a855f7", "#ff3cac"], text="Runs")
            fig.update_layout(coloraxis_showscale=False)
            fig.update_traces(textposition="outside")
            st.plotly_chart(style_chart(fig, 450), use_container_width=True)
        else:
            st.info("No total_runs or match_id columns found.")
    with c2:
        if "batter" in fd.columns and "batter_runs" in fd.columns and not fd.empty:
            batter_runs = fd.groupby("batter")["batter_runs"].sum().nlargest(10).sort_values().reset_index(name="Runs")
            batter_runs = batter_runs.rename(columns={"batter": "Player"})
            fig = px.bar(batter_runs, x="Runs", y="Player", orientation="h",
                         title="🚀 Top 10 Run Scorers", color="Runs",
                         color_continuous_scale=["#164e63", "#0891b2", "#00f5ff"], text="Runs")
            fig.update_layout(coloraxis_showscale=False, yaxis_title="")
            fig.update_traces(textposition="outside")
            st.plotly_chart(style_chart(fig, 450), use_container_width=True)
        else:
            st.info("Player run analysis needs batter and batter_runs columns.")

    if "batter_runs" in fd.columns:
        runs_distribution = fd["batter_runs"].value_counts().reindex([0, 1, 2, 3, 4, 6], fill_value=0)
        distribution = pd.DataFrame({"Runs off bat": runs_distribution.index.astype(str), "Deliveries": runs_distribution.values})
        fig = px.bar(distribution, x="Runs off bat", y="Deliveries", title="🎆 Runs off the Bat Distribution",
                     color="Runs off bat", color_discrete_sequence=COLORS)
        st.plotly_chart(style_chart(fig, 330), use_container_width=True)

# --------------------- PAGE: PLAYER PERFORMANCE --------------
elif page == "Player Performance Lab":
    section_heading("🎯", "PLAYER", " PERFORMANCE LAB")
    if "batter" in fd.columns and "batter_runs" in fd.columns:
        player_names = sorted(fd["batter"].dropna().astype(str).unique())
        if player_names:
            player = st.selectbox("Choose a batter", player_names)
            pdata = fd[fd["batter"].astype(str) == player]
            runs = int(pdata["batter_runs"].sum())
            fours = int((pdata["batter_runs"] == 4).sum())
            sixes = int((pdata["batter_runs"] == 6).sum())
            # A delivery count is not always the official balls-faced count:
            # wides are excluded if extras_type identifies them.
            balls = len(pdata)
            if "extras_type" in pdata.columns:
                balls = int((pdata["extras_type"].astype(str).str.lower() != "wides").sum())
            strike_rate = (runs / balls * 100) if balls else 0
            c1, c2, c3, c4 = st.columns(4)
            player_kpis = [("🏏", "RUNS", f"{runs:,}"), ("💥", "FOURS", f"{fours:,}"),
                           ("🚀", "SIXES", f"{sixes:,}"), ("⚡", "STRIKE RATE*", f"{strike_rate:.2f}")]
            for col, (icon, label, value) in zip([c1,c2,c3,c4], player_kpis):
                with col:
                    st.markdown(f'<div class="kpi-card"><div class="kpi-icon">{icon}</div><div class="kpi-label">{label}</div><div class="kpi-value">{value}</div></div>', unsafe_allow_html=True)
            st.caption("*Approximate strike rate; exact balls-faced handling depends on the source dataset.")
            if "season" in fm.columns:
                player_matches = set(fm["id"].dropna()) if "id" in fm.columns else set()
                pfd = fd[fd["batter"].astype(str) == player].copy()
                if "match_id" in pfd.columns:
                    seasonal = pfd.groupby("match_id")["batter_runs"].sum().reset_index(name="Runs")
                    if "id" in fm.columns and "season" in fm.columns:
                        seasonal = seasonal.merge(fm[["id","season"]], left_on="match_id", right_on="id", how="left")
                        seasonal = seasonal.groupby("season")["Runs"].sum().reset_index()
                        seasonal["season"] = seasonal["season"].astype(str)
                        fig = px.line(seasonal, x="season", y="Runs", markers=True,
                                      title=f"📈 {player} — Runs by Season",
                                      color_discrete_sequence=["#00f5ff"])
                        fig.update_traces(line=dict(width=3), marker=dict(size=9))
                        st.plotly_chart(style_chart(fig), use_container_width=True)
        else:
            st.info("No batters found for the selected filters.")
    else:
        st.info("Player analysis requires batter and batter_runs columns in deliveries.csv.")

# --------------------- PAGE: TOP WICKET TAKERS ---------------
elif page == "Top Wicket Takers":
    section_heading("🎯", "TOP WICKET", " TAKERS")
    st.caption("Wickets credited to bowlers where dismissal type is available. Run-outs and other non-bowler dismissals are excluded.")
    if not top_wickets.empty:
        top_n = st.slider("Number of bowlers", min_value=5, max_value=min(25, max(5, len(top_wickets))), value=min(10, max(5, len(top_wickets))))
        top_n_df = top_wickets.head(top_n).sort_values("Wickets")
        c1, c2 = st.columns([3, 2])
        with c1:
            fig = px.bar(top_n_df, x="Wickets", y="Bowler", orientation="h",
                         title=f"🎯 Top {top_n} Wicket Takers", color="Wickets",
                         color_continuous_scale=["#164e63", "#a855f7", "#00f5ff"], text="Wickets")
            fig.update_layout(coloraxis_showscale=False, yaxis_title="")
            fig.update_traces(textposition="outside", marker_line_width=0)
            st.plotly_chart(style_chart(fig, max(390, top_n * 32)), use_container_width=True)
        with c2:
            leader = top_wickets.iloc[0]
            st.markdown(f"""<div class="kpi-card">
                <div class="kpi-icon">👑</div><div class="kpi-label">TOP WICKET TAKER</div>
                <div class="kpi-value" style="font-size:22px">{leader['Bowler']}</div>
                <div class="kpi-note">{int(leader['Wickets'])} credited wickets</div>
            </div>""", unsafe_allow_html=True)
            st.dataframe(top_wickets.head(top_n), use_container_width=True, hide_index=True)
    else:
        st.warning("Cannot calculate top wicket takers. Check that deliveries.csv has a bowler column and wicket information.")

# --------------------- PAGE: MATCH EXPLORER ------------------
elif page == "Match Explorer":
    section_heading("🔎", "MATCH", " EXPLORER")
    if not fm.empty:
        display_cols = [c for c in ["id","season","date","team1","team2","winner","venue","player_of_match"] if c in fm.columns]
        table = fm[display_cols].copy()
        st.dataframe(table, use_container_width=True, hide_index=True, height=420)
        st.download_button("⬇️ Download filtered matches", table.to_csv(index=False).encode("utf-8"),
                           file_name="ipl_filtered_matches.csv", mime="text/csv")
    else:
        st.warning("No matches for the selected filters. Select more seasons or teams in the sidebar.")

# --------------------------- FOOTER --------------------------
st.markdown("""
<div class="footer">
  🏏 <span>IPL PULSE</span> — INTERACTIVE CRICKET ANALYTICS<br><br>
  Built with Python · Streamlit · Pandas · Plotly<br><br>
  <span>TURN DATA INTO INSIGHTS ✦</span>
</div>
""", unsafe_allow_html=True)