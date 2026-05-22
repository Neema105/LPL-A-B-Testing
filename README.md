LPL A/B Testing
===============

Python analysis project for loading LPL match data into PostgreSQL, running A/B tests for First Dragon and Void Grubs, and exporting CSV and Excel summary outputs.

Setup
-----

Create the PostgreSQL database named `lolanalytics`, install dependencies, and set `DATABASE_URL`.

```powershell
python -m venv .venv
.\.venv\Scripts\pip install -r requirements.txt
$env:DATABASE_URL = "postgresql://postgres:YOUR_PASSWORD@localhost:5432/lolanalytics"
```

Run
---

```powershell
.\.venv\Scripts\python.exe scripts\load_data.py
.\.venv\Scripts\python.exe scripts\create_stats_summary.py
.\.venv\Scripts\python.exe scripts\ab_testing.py
.\.venv\Scripts\python.exe scripts\excel_export.py
```

The final workbook is written to `outputs/lpl_executive_summary.xlsx`.
