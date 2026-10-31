# IPL Match & Player Performance Analysis

A beginner-friendly Data Analyst project using Python, Pandas, Matplotlib, Seaborn, Jupyter Notebook, and Power BI.

## Dataset
Download compatible historical IPL CSV files from [Kaggle IPL dataset search](https://www.kaggle.com/search?q=IPL+dataset). Put `matches.csv` and `deliveries.csv` in `dataset/`.

## Install
Use Python 3.10+ and run these commands from the project root:

```bash
python -m venv .venv
```

Windows:
```bash
.venv\Scripts\activate
```

macOS/Linux:
```bash
source .venv/bin/activate
```

Then:
```bash
pip install -r requirements.txt
```

## Run scripts in this order
```bash
python src/data_cleaning.py
python src/exploratory_data_analysis.py
python src/player_performance.py
```

Generated cleaned files and summary tables go to `outputs/cleaned_data/`. PNG charts go to `outputs/charts/`.

## Power BI
1. Open Power BI Desktop.
2. Use **Get data > Text/CSV** to import the cleaned CSVs and summary tables.
3. Link match IDs between the match and delivery tables (verify the key column names).
4. Add KPI cards, team wins, top batters, top bowlers, toss results, venue analysis, season-wise runs, and season/team/venue slicers.
5. Save as `dashboard/IPL_Performance_Dashboard.pbix`.

## Notes
Dataset schemas vary. The cleaning script handles common column-name variations, but check your actual columns if an error occurs. No-result matches may have missing winners. Bowling summaries exclude common non-bowler-credited dismissals when dismissal type is available. Only report insights after verifying the actual outputs from your dataset.
