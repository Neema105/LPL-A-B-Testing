from sqlalchemy import create_engine, text
import os

DB_URL = os.environ['DATABASE_URL']

engine = create_engine(DB_URL)

with engine.connect() as conn:
    conn.execute(text("""
        CREATE OR REPLACE VIEW lpl_stats_summary AS
        SELECT
            side,
            'First Dragon'                          AS objective,
            COUNT(*) FILTER (WHERE got_fd = 1)      AS treatment_n,
            COUNT(*) FILTER (WHERE got_fd = 0)      AS control_n,
            ROUND(AVG(result) FILTER (WHERE got_fd = 1)::numeric, 4)
                                                    AS treatment_wr,
            ROUND(AVG(result) FILTER (WHERE got_fd = 0)::numeric, 4)
                                                    AS control_wr,
            ROUND(
                AVG(result) FILTER (WHERE got_fd = 1)::numeric -
                AVG(result) FILTER (WHERE got_fd = 0)::numeric, 4)
                                                    AS delta
        FROM lpl_ab_analysis
        GROUP BY side

        UNION ALL

        SELECT
            side,
            'More Grubs'                                        AS objective,
            COUNT(*) FILTER (WHERE got_more_grubs = 1)          AS treatment_n,
            COUNT(*) FILTER (WHERE got_more_grubs = 0)          AS control_n,
            ROUND(AVG(result) FILTER (WHERE got_more_grubs = 1)::numeric, 4)
                                                                AS treatment_wr,
            ROUND(AVG(result) FILTER (WHERE got_more_grubs = 0)::numeric, 4)
                                                                AS control_wr,
            ROUND(
                AVG(result) FILTER (WHERE got_more_grubs = 1)::numeric -
                AVG(result) FILTER (WHERE got_more_grubs = 0)::numeric, 4)
                                                                AS delta
        FROM lpl_ab_analysis
        GROUP BY side

        ORDER BY side, objective
    """))

    conn.commit()
    print('lpl_stats_summary view created successfully')

    result = conn.execute(text("SELECT * FROM lpl_stats_summary"))
    rows = result.fetchall()
    print()
    print(f'{"SIDE":<6} {"OBJECTIVE":<15} {"TREAT_N":<10} {"CTRL_N":<10} {"TREAT_WR":<12} {"CTRL_WR":<12} {"DELTA":<8}')
    print('-' * 70)
    for row in rows:
        print(f'{row[0]:<6} {row[1]:<15} {row[2]:<10} {row[3]:<10} {row[4]:<12} {row[5]:<12} {row[6]:<8}')
