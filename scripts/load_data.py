import pandas as pd
from sqlalchemy import create_engine, text
from pathlib import Path
import os

DB_URL = os.environ['DATABASE_URL']
BASE_DIR = Path(__file__).resolve().parents[1]
CSV_PATH = BASE_DIR / 'data' / 'lol_raw.csv'

engine = create_engine(DB_URL)

print('Loading raw data...')
df = pd.read_csv(CSV_PATH, low_memory=False)
df.to_sql('lpl_raw', engine, if_exists='replace', index=False)
print(f'Loaded {len(df)} rows into lpl_raw')

with engine.connect() as conn:

    conn.execute(text("""
        CREATE OR REPLACE VIEW lpl_teams AS
        SELECT * FROM lpl_raw
        WHERE league = 'LPL'
        AND position = 'team'
    """))

    conn.execute(text("""
        CREATE OR REPLACE VIEW lpl_ab_analysis AS
        SELECT
            gameid, date, patch, teamname, side, result,
            gamelength / 60.0 AS game_mins,
            CASE WHEN firstdragon = 1 THEN 1 ELSE 0 END AS got_fd,
            CASE WHEN void_grubs > opp_void_grubs THEN 1 ELSE 0 END AS got_more_grubs,
            CASE
                WHEN firstdragon = 1 AND void_grubs > opp_void_grubs THEN 'FD + More Grubs'
                WHEN firstdragon = 1 THEN 'FD Only'
                WHEN void_grubs > opp_void_grubs THEN 'More Grubs Only'
                ELSE 'Neither'
            END AS scenario,
            golddiffat15, xpdiffat15, kills, deaths,
            firstbaron, firsttower, turretplates, opp_turretplates
        FROM lpl_teams
    """))

    conn.commit()

print('Views created successfully')
print('Ready for 01_ab_testing.py')
